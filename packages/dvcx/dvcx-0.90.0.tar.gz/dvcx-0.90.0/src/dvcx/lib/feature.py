import inspect
import re
import warnings
from collections.abc import Sequence
from types import GenericAlias
from typing import Any, ClassVar, get_args, get_origin

import attrs
from pydantic import BaseModel

from dvcx.lib.utils import convert_type_to_dvcx
from dvcx.query import C
from dvcx.query.udf import UDFOutputSpec
from dvcx.sql.types import (
    JSON,
    Array,
    NullType,
)

# Disable Pydantic warning, see https://github.com/iterative/dvcx/issues/1285
warnings.filterwarnings(
    "ignore",
    message="Field name .* shadows an attribute in parent",
    category=UserWarning,
)


class Feature(BaseModel):
    """A base class for defining data classes that serve as inputs and outputs for
    DataFrame processing functions like `map()`, `generate()`, etc. Inherits from
    `pydantic`'s BaseModel, allowing for data validation and definition.
    """

    _expand_name: ClassVar[bool] = True
    _delimiter: ClassVar[str] = "__"
    _is_file: ClassVar[bool] = False

    def get_value(self, *args: Any, **kwargs: Any) -> Any:
        name = self.__class__.__name__
        raise NotImplementedError(f"value is not defined for feature class {name}")

    def _get_value_with_check(self, *args: Any, **kwargs: Any) -> Any:
        signature = inspect.signature(self.get_value)
        for i, (name, prm) in enumerate(signature.parameters.items()):
            if prm.default == inspect.Parameter.empty:
                if i < len(args):
                    continue
                if name not in kwargs:
                    raise ValueError(
                        f"unable to get value for class {self.__class__.__name__}"
                        f" due to a missing parameter {name} in get_value()"
                    )

        return self.get_value(*args, **kwargs)

    @classmethod
    def __pydantic_init_subclass__(cls):
        for name, field_info in cls.model_fields.items():
            attr_value = _resolve(cls, name, field_info, cls._prefix())
            setattr(cls, name, RestrictedAttribute(attr_value, cls, name))

    @classmethod
    def _prefix(cls) -> str:
        return cls._normalize(cls.__name__)

    @classmethod
    def _normalize(cls, name: str) -> str:
        if (
            cls._expand_name
            and cls._delimiter
            and cls._delimiter.lower() in name.lower()
        ):
            raise RuntimeError(
                f"variable '{name}' cannot be used because it contains {cls._delimiter}"
            )
        return Feature._to_snake_case(name)

    @staticmethod
    def _to_snake_case(name: str) -> str:
        """Convert a CamelCase name to snake_case."""
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    @staticmethod
    def _iter_fields(fields):
        for name, f_info in fields.items():
            yield name, f_info.annotation, f_info.is_required()

    @classmethod
    def _flatten_full_schema(cls, fields, name_path):
        for name, anno, is_required in cls._iter_fields(fields):
            name = cls._normalize(name)

            orig = get_origin(anno)
            if orig == list:
                anno = get_args(anno)
                if isinstance(anno, tuple):
                    anno = anno[0]
                is_list = True
            else:
                is_list = False

            expanded_name = name
            if cls._expand_name:
                lst = [cls._prefix(), *name_path, name]
                expanded_name = cls._delimiter.join(lst)

            if Feature.is_feature_class(anno):
                if is_list:
                    yield expanded_name, Array(JSON), is_required
                else:
                    yield from cls._flatten_full_schema(
                        anno.model_fields, [*name_path, name]
                    )
            else:
                typ = convert_type_to_dvcx(anno)
                if is_list:
                    typ = Array(typ)
                yield expanded_name, typ, is_required

    @classmethod
    def is_feature_class(cls, anno):
        return (
            inspect.isclass(anno)
            and not isinstance(anno, GenericAlias)
            and issubclass(anno, Feature)
        )

    @classmethod
    def _to_udf_spec(cls):
        full_schema = cls._flatten_full_schema(cls.model_fields, [])
        return [(name, typ) for name, typ, is_required in full_schema]

    @staticmethod
    def _features_to_udf_spec(fr_classes: Sequence[type["Feature"]]) -> UDFOutputSpec:
        return dict(
            item
            for b in fr_classes
            for item in b._to_udf_spec()  # type: ignore[attr-defined]
        )

    def _flatten_fields_values(self, fields, dump):
        for name, anno, _ in self._iter_fields(fields):
            value = dump[name]
            if Feature.is_feature_class(anno):
                yield from self._flatten_fields_values(anno.model_fields, value)
            else:
                yield value

    def _flatten(self):
        return tuple(self._flatten_fields_values(self.model_fields, self.model_dump()))

    @staticmethod
    def _flatten_list(objs):
        return tuple(val for obj in objs for val in obj._flatten())

    @classmethod
    def _unflatten_with_path(cls, dump, path):
        res = {}
        for name, anno, _ in Feature._iter_fields(cls.model_fields):
            name_norm = cls._normalize(name)
            if cls._expand_name:
                curr_path = path + cls._delimiter + name_norm
            else:
                curr_path = name_norm

            if Feature.is_feature_class(anno):
                val = anno._unflatten_with_path(dump, curr_path)
                res[name] = val
            else:
                res[name] = dump[curr_path]
        return cls(**res)

    @classmethod
    def _unflatten(cls, dump):
        return cls._unflatten_with_path(dump, cls._prefix())


class RestrictedAttribute:
    """Descriptor implementing an attribute that can only be accessed through
    the defining class and not from subclasses or instances.

    Since it is a non-data descriptor, instance dicts have precedence over it.
    Cannot be used with slotted classes.
    """

    def __init__(self, value, cls=None, name=None):
        self.cls = cls
        self.value = value
        self.name = name

    def __get__(self, instance, owner):
        if owner is not self.cls:
            raise AttributeError(
                f"'{type(owner).__name__}' object has no attribute '{self.name}'"
            )
        if instance is not None:
            raise RuntimeError(
                f"Invalid attempt to access class attribute '{self.name}' through "
                f"'{type(owner).__name__}' instance"
            )
        return self.value

    def __set_name__(self, cls, name):
        self.cls = cls
        self.name = name


@attrs.define
class FeatureAttributeWrapper:
    cls: type[Feature]
    prefix: str

    def __getattr__(self, name):
        field_info = self.cls.model_fields.get(name)
        if field_info:
            return _resolve(self.cls, name, field_info, prefix=self.prefix)
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )


def _resolve(cls, name, field_info, prefix):
    """Resolve feature attributes so they can be used in select(), join()
    and similar functions.

    Users just use `MyClass.sub_attr1.sub_attr2.field` and it will return a DB column
    with a proper name (with default naming - `my_class__sub_attr1__sub_attr2__field`).
    """
    anno = field_info.annotation
    norm_name = cls._normalize(name)

    if not cls.is_feature_class(anno):
        try:
            anno_sql_class = convert_type_to_dvcx(anno)
        except TypeError:
            anno_sql_class = NullType
        if cls._expand_name:
            return C(cls._delimiter.join([prefix, norm_name]), anno_sql_class)
        return C(norm_name, anno_sql_class)

    if not cls._expand_name:
        return FeatureAttributeWrapper(anno, "")

    new_prefix_value = cls._delimiter.join([prefix, norm_name])
    return FeatureAttributeWrapper(anno, new_prefix_value)


class ShallowFeature(Feature):
    _expand_name: ClassVar[bool] = False
