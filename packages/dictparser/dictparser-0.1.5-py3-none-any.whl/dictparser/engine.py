import types
import typing
import collections.abc
import copy
import dataclasses
import sys
import pathlib

from abc import ABC, abstractmethod

import yaml


_CLASS_DATA = "__dictparser_class_data__"
_FROM_DICT_METHOD = "from_dict"
_FROM_FILE_METHOD = "from_file"
_AS_DICT_METHOD = "as_dict"


class MISSING:
    pass


class ClassData:
    def __init__(self):
        self.fields = {}
        self.result_cls = MISSING
        self.has_required = False
        self.ignore_extra = False


class TypeData(ABC):
    def __init__(self, field_type, res_types):
        self.field_type = field_type
        self.res_types = res_types

    def get_value(self, data):
        res = self._convert_value(data)
        self._validate_res_type(res)
        return res

    @abstractmethod
    def _convert_value(self, data):
        pass

    def _validate_res_type(self, res):
        for i in self.res_types:
            if isinstance(res, i):
                return

        raise RuntimeError(f"Converted value does not match expected result type: {type(res)} vs {self.res_types}")


class HasFromDictTypeData(TypeData):
    def _convert_value(self, data):
        if type(data) in self.res_types:
            return data
        else:
            return getattr(self.field_type, _FROM_DICT_METHOD)(data)


class NullTypeData(TypeData):
    def _convert_value(self, data):
        if data is None:
            return None
        else:
            raise RuntimeError(f"Invalid data type '{data.__class__}' for field type of None")


class ConstructorTypeData(TypeData):
    def __init__(self, field_type, res_types, func):
        super().__init__(field_type, res_types)
        self.func = func

    def _convert_value(self, data):
        if data in self.res_types:
            return data
        else:
            return self.func(data)


class ListTypeData(TypeData):
    def __init__(self, field_type, res_types, item_type_data: TypeData):
        super().__init__(field_type, res_types)
        self.item_type_data = item_type_data

    def _convert_value(self, data):
        return self.res_types[0](
            [self.item_type_data.get_value(v) for v in data]
        )


class DictTypeData(TypeData):
    def __init__(self, field_type, res_types, key_type_data: TypeData, value_type_data: TypeData):
        super().__init__(field_type, res_types)
        self.key_type_data = key_type_data
        self.value_type_data = value_type_data

    def _convert_value(self, data):
        return self.res_types[0](
            [(self.key_type_data.get_value(k), self.value_type_data.get_value(v)) for k, v in data.items()]
        )


class OptionalTypeData(TypeData):
    def __init__(self, field_type, res_types, item_type_data: TypeData):
        super().__init__(field_type, res_types)
        self.item_type_data = item_type_data

    def _convert_value(self, data):
        if data is None:
            return None
        else:
            return self.item_type_data.get_value(data)


def parse_field_type(field_type) -> TypeData:
    if hasattr(field_type, _FROM_DICT_METHOD):
        return HasFromDictTypeData(field_type, [field_type])

    elif field_type == type(None) or field_type is None:
        return NullTypeData(field_type, [type(None)])

    elif _get_origin(field_type) is not None:
        origin = _get_origin(field_type)

        if _is_union_type(field_type):
            args = _get_args(field_type)

            if len(args) == 2:
                if args[0] is None or args[0] == type(None):
                    arg_type_data = parse_field_type(args[1])
                    return OptionalTypeData(field_type, [type(None)] + arg_type_data.res_types, arg_type_data)

                elif args[1] is None or args[1] == type(None):
                    arg_type_data = parse_field_type(args[0])
                    return OptionalTypeData(field_type, [type(None)] + arg_type_data.res_types, arg_type_data)

            raise NotImplementedError("Union type with <> 2 arguments is not supported")

        elif origin in (list, typing.List):
            args = _get_args(field_type)

            if len(args) != 1:
                raise RuntimeError("List type annotation has an amount of argument types different than 1")

            return ListTypeData(field_type, [list], parse_field_type(args[0]))

        elif origin in (dict, typing.Dict):
            args = _get_args(field_type)

            if len(args) != 2:
                raise RuntimeError("Dict type annotation has an amount of argument types different than 2")

            return DictTypeData(field_type, [dict], parse_field_type(args[0]), parse_field_type(args[1]))

        #elif origin in (tuple, ): This is alot more complicated than this
        #    args = _get_args(field_type)
        #    return ListTypeData(field_type, [tuple], parse_field_type(args[0]))

        else:
            raise NotImplementedError(f"'origin {origin}' not implemented")

    elif field_type in (bool, int, float, complex, str, bytes, bytearray, pathlib.Path):
        return ConstructorTypeData(field_type, [field_type], field_type)

    else:
        raise NotImplementedError(f"Type {field_type} not implemented")


class Field:
    def __init__(
        self,
        field_name,
        field_type_data,
        data_key,
        default: typing.Any = MISSING,
        default_factory: typing.Any = MISSING
    ):
        self.field_name = field_name
        self.field_type_data = field_type_data
        self.data_key = data_key
        self.default = None
        self.default_factory = None
        self.has_default = False
        self.required = True

        if default is not MISSING:
            self.has_default = True
            self.required = False
            self.default = default

        elif default_factory is not MISSING:
            self.has_default = True
            self.required = False
            self.default_factory = default_factory

    @classmethod
    def from_type(cls, field_name, field_type, default=MISSING):
        data_key = field_name
        default_factory = MISSING

        field_type_data = parse_field_type(field_type)

        if default is not MISSING:
            default = field_type_data.get_value(default)

            if default.__class__.__hash__ is None:
                def copy_factory(default):
                    return lambda : copy.deepcopy(default)

                default_factory = copy_factory(default)
                default = MISSING

        return cls(field_name, field_type_data, data_key, default=default, default_factory=default_factory)

    def get_value(self, data):
        return self.field_type_data.get_value(data)

    def get_default(self):
        if self.default_factory:
            return self.default_factory()
        else:
            return self.default


if sys.version_info >= (3, 11):
    T = typing.TypeVar("T")

    def process_class(cls: type[T], kw_only=False) -> type[T]:
        return process_class_inner(cls, kw_only)
else:
    def process_class(cls, kw_only=False):
        return process_class_inner(cls, kw_only)


def process_class_inner(cls, kw_only):
    fields = {}

    for base in cls.__mro__[-1:0:-1]:
        base_data = getattr(base, _CLASS_DATA, None)
        if base_data is not None:
            for field in base_data.fields.values():
                fields[field.field_name] = field

    if hasattr(cls, "__annotations__"):
        for field_name, field_type in cls.__annotations__.items():
            if hasattr(cls, field_name):
                default = getattr(cls, field_name)
                delattr(cls, field_name)
                field = Field.from_type(field_name, field_type, default)
            else:
                field = Field.from_type(field_name, field_type)

            fields[field.field_name] = field

    #
    #
    #
    _class_data = ClassData()
    setattr(cls, _CLASS_DATA, _class_data)

    _class_data.fields = fields

    for field in _class_data.fields.values():
        if not field.has_default:
            _class_data.has_required = True
            break

    _class_data.result_cls = cls

    #
    #
    #
    _setattr_method_from_dict(cls)
    _setattr_method_from_file(cls)
    _setattr_method_as_dict(cls)

    return dataclasses.dataclass(cls)


if sys.version_info >= (3, 10):
    def _get_origin(t):
        return typing.get_origin(t)


    def _is_union_type(t):
        origin = _get_origin(t)
        return origin in (types.UnionType, typing.Union)


    def _get_args(t):
        return list(typing.get_args(t))
else:
    def _get_origin(t):
        if hasattr(t, "__origin__"):
            return t.__origin__
        else:
            return None


    def _is_union_type(t):
        origin = _get_origin(t)
        return origin in (typing.Union, )


    def _get_args(t):
        return list(t.__args__)


def _setattr_method_from_dict(cls):
    if hasattr(cls, _FROM_DICT_METHOD):
        return

    def from_dict(cls, data):
        class_data = getattr(cls, _CLASS_DATA)

        if not isinstance(data, collections.abc.Mapping):
            raise RuntimeError("data is not a dict like value")

        args = {}
        keys = set(data.keys())

        for field in class_data.fields.values():
            if field.data_key in data:
                args[field.field_name] = field.get_value(data[field.data_key])
                keys.remove(field.data_key)
            elif field.has_default:
                args[field.field_name] = field.get_default()
            elif field.required:
                raise RuntimeError(f"Required field '{field.field_name}' is missing")
            else:
                raise RuntimeError("ups")

        if len(keys) > 0 and not class_data.ignore_extra:
            raise RuntimeError(f"Extra data keys: {list(keys)}")

        result_cls = class_data.result_cls
        return result_cls(**args)

    from_dict.__qualname__ = f"{cls.__qualname__}.from_dict"

    setattr(cls, _FROM_DICT_METHOD, classmethod(from_dict))


def _setattr_method_from_file(cls):
    if hasattr(cls, _FROM_FILE_METHOD):
        return

    def from_file(cls, file):
        with open(file, "rt", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls.from_dict(data)

    from_file.__qualname__ = f"{cls.__qualname__}.from_file"

    setattr(cls, _FROM_FILE_METHOD, classmethod(from_file))


def _setattr_method_as_dict(cls):
    if hasattr(cls, _AS_DICT_METHOD):
        return

    def as_dict(self):
        return dataclasses.asdict(self)

    as_dict.__qualname__ = f"{cls.__qualname__}.as_dict"

    setattr(cls, _AS_DICT_METHOD, as_dict)
