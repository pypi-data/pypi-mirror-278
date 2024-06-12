from collections.abc import Sequence
from typing import Any, Union, get_args, get_origin

from pydantic import BaseModel, create_model

from dvcx.lib.feature import Feature, ShallowFeature
from dvcx.lib.reader import FeatureReader
from dvcx.lib.utils import TYPE_FROM_DVCX, TYPE_TO_DVCX, convert_type_to_dvcx
from dvcx.query.schema import Column
from dvcx.sql.types import NullType, SQLType

FeatureLike = Union[type["Feature"], FeatureReader, Column, str]


class ColumnFeature(ShallowFeature):
    def _get_column_value(self):
        raise NotImplementedError("value is not defined for class ColumnFeature")


feature_registry: dict[type[BaseModel], type[Feature]] = {}


def pydantic_to_feature(data_cls: type[BaseModel]) -> type[Feature]:
    if data_cls in feature_registry:
        return feature_registry[data_cls]

    fields = {}
    for name, field_info in data_cls.model_fields.items():
        anno = field_info.annotation
        if anno not in TYPE_TO_DVCX:
            orig = get_origin(anno)
            if orig == list:
                anno = get_args(anno)  # type: ignore[assignment]
                if isinstance(anno, Sequence):
                    anno = anno[0]  # type: ignore[unreachable]
                is_list = True
            else:
                is_list = False

            try:
                convert_type_to_dvcx(anno)
            except TypeError:
                if not Feature.is_feature_class(anno):  # type: ignore[arg-type]
                    anno = pydantic_to_feature(anno)  # type: ignore[arg-type]

            if is_list:
                anno = list[anno]  # type: ignore[valid-type]
        fields[name] = (anno, field_info.default)

    cls = create_model(
        data_cls.__name__,
        __base__=(data_cls, Feature),  # type: ignore[call-overload]
        **fields,
    )
    feature_registry[data_cls] = cls
    return cls


class FeatureTypes:
    @classmethod
    def column_class(
        cls,
        name: Union[str, Column],
        typ=Any,
        default=None,
        value_func=None,
    ):
        """Creating a column feature dynamically.
        :param fields:
            **name: <name> is string or a Column. For Column, a type can be specified.
            **typ: type of a column. Default is `Any`.
            **default: an optional default value
            **value_func: an optional function for get_value()
        """

        new_class = ColumnFeature

        if isinstance(name, Column):
            if typ is Any and not isinstance(name.type, NullType):
                if isinstance(name.type, SQLType):
                    typ = TYPE_FROM_DVCX.get(type(name.type), Any)  # type: ignore[arg-type]
                else:
                    typ = type(name.type)
            name = name.name

        fields = {name: (typ, default)}
        new_class_name = f"{new_class.__name__}_{name}"

        obj = create_model(
            new_class_name,
            __base__=new_class,  # type: ignore[call-overload]
            **fields,
        )

        obj._get_column_value = lambda self: getattr(self, name)

        if value_func:
            obj.get_value = lambda self: value_func(obj._get_column_value(self))
        else:
            obj.get_value = obj._get_column_value

        return obj

    @classmethod
    def column_classes(
        cls, fields: dict[Union[str, Column], tuple[type, Any]], value_func=None
    ) -> type:
        """Creating columns dynamically.
        :param fields:
            **fields: Attributes of the new model. They should be passed in the format:
            `<name>=(<type>, <default value>)` or `<name>=(<type>, <FieldInfo>)`
            where <name> is string or a Column
        """
        fields_text_keys = {
            key.name if isinstance(key, Column) else key: value
            for key, value in fields.items()
        }

        cls_suffix = "_".join(fields_text_keys.keys())
        new_class = ShallowFeature

        obj = create_model(
            f"{new_class.__name__}_{cls_suffix}",
            __base__=new_class,  # type: ignore[call-overload]
            **fields_text_keys,
        )

        obj._get_column_value = lambda self: tuple(
            [getattr(self, name) for name in fields_text_keys]
        )

        if value_func:
            obj.get_value = lambda self: value_func(self)
        else:
            obj.get_value = obj._get_column_value

        return obj

    @classmethod
    def _to_features(cls, *fr_classes: FeatureLike) -> Sequence[type["Feature"]]:
        features = []
        for fr in fr_classes:
            if isinstance(fr, (str, Column)):
                features.append(cls.column_class(fr))
            elif isinstance(fr, FeatureReader):
                features += cls._to_features(fr.fr_class)
            else:
                features.append(fr)
        return features
