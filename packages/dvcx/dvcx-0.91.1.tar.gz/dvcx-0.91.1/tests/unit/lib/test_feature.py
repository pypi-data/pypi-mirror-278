from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional, Union, get_args

import pytest
from pydantic import BaseModel, Field, ValidationError

from dvcx.lib.dataset import C
from dvcx.lib.feature import (
    Feature,
    ShallowFeature,
)
from dvcx.lib.feature_types import FeatureTypes, pydantic_to_feature
from dvcx.sql.types import JSON, Array, Binary, Boolean, DateTime, Float, Int, String


class FileBasic(ShallowFeature):
    parent: str = Field(default="")
    name: str
    size: int = Field(default=0)


class FileInfo(FileBasic):
    location: dict = Field(default={})


class FileInfoEx(ShallowFeature):
    f_info: FileInfo
    type_id: int


class MyNestedClass(Feature):
    type: int
    Name: str = Field(default="test1")


class MyTest(Feature):
    ThisIsName: str
    subClass: MyNestedClass  # noqa: N815


def test_flatten_schema():
    schema = FileInfo._to_udf_spec()

    assert len(schema) == 4
    assert [item[0] for item in schema] == ["parent", "name", "size", "location"]
    assert [item[1] for item in schema] == [String, String, Int, JSON]


def test_type_datatype():
    class Test1(Feature):
        d: datetime

    schema = Test1._to_udf_spec()
    assert schema[0][1] == DateTime


def test_type_optional_int():
    class Test1(Feature):
        d: Optional[int] = 23

    schema = Test1._to_udf_spec()
    assert schema[0][1] == Int


def test_type_bytes():
    class Test1(Feature):
        d: bytes

    schema = Test1._to_udf_spec()
    assert schema[0][1] == Binary


def test_type_array():
    class Test1(Feature):
        d: list

    schema = Test1._to_udf_spec()
    assert type(schema[0][1]) == Array


def test_type_arrays():
    class Test1(Feature):
        d1: list[int]
        d2: list[float]

    schema = Test1._to_udf_spec()

    assert schema[0][1].to_dict() == {"item_type": {"type": "Int"}, "type": "Array"}
    assert schema[1][1].to_dict() == {"item_type": {"type": "Float"}, "type": "Array"}


def test_type_array_of_arrays():
    class Test1(Feature):
        d1: list[list[int]]

    schema = Test1._to_udf_spec()

    type1 = schema[0][1]
    assert list == type1.python_type
    assert list == type1.impl.item_type.python_type
    assert int == type1.impl.item_type.impl.item_type.python_type


def test_type_json():
    class Test1(Feature):
        d: dict

    schema = Test1._to_udf_spec()
    assert schema[0][1] == JSON


def test_type_bool():
    class Test1(Feature):
        d: bool

    schema = Test1._to_udf_spec()
    assert schema[0][1] == Boolean


def test_type_typed_json():
    class Test1(Feature):
        d: Optional[dict[str, int]]

    schema = Test1._to_udf_spec()
    assert schema[0][1] == JSON


def test_unknown_type():
    class Test1(Feature):
        d: Optional[Decimal]

    with pytest.raises(TypeError):
        Test1._to_udf_spec()


def test_flatten_nested_schema():
    schema = FileInfoEx._to_udf_spec()

    assert len(schema) == 5
    assert [item[0] for item in schema] == [
        "parent",
        "name",
        "size",
        "location",
        "type_id",
    ]
    assert [item[1] for item in schema] == [String, String, Int, JSON, Int]


def test_flatten_nested_schema_shallow():
    class MyTest1(Feature):
        a: int = Field(default=33)

    class MyTest2(Feature):
        next2: MyTest1

    class MyTest3(Feature):
        next3: MyTest2

    schema = MyTest3(next3=MyTest2(next2=MyTest1()))._to_udf_spec()
    assert [item[0] for item in schema] == ["my_test3__next3__next2__a"]

    class MyTest3Shallow(ShallowFeature):
        next3: MyTest2

    shallow_schema = MyTest3Shallow(next3=MyTest2(next2=MyTest1()))._to_udf_spec()
    assert [item[0] for item in shallow_schema] == ["a"]


def test_flatten_schema_list():
    t1 = FileInfo(name="test1")
    t2 = FileInfo(name="t2", parent="pp1")
    res = Feature._features_to_udf_spec([t1, t2])
    assert len(t1.model_dump()) == len(res)


def test_flatten_basic():
    vals = FileBasic(parent="hello", name="world", size=123)._flatten()
    assert vals == ("hello", "world", 123)


def test_flatten_with_json():
    t1 = FileInfo(parent="prt4", name="test1", size=42, location={"ee": "rr"})
    assert t1._flatten() == ("prt4", "test1", 42, {"ee": "rr"})


def test_flatten_with_empty_json():
    with pytest.raises(ValidationError):
        FileInfo(parent="prt4", name="test1", size=42, location=None)


def test_flatten_with_accepted_empty_json():
    class Test1(Feature):
        d: Optional[dict]

    assert Test1(d=None)._flatten() == (None,)


def test_flatten_nested():
    t0 = FileInfo(parent="sfo", name="sf", size=567, location={"42": 999})
    t1 = FileInfoEx(f_info=t0, type_id=1849)

    assert t1._flatten() == ("sfo", "sf", 567, {"42": 999}, 1849)


def test_flatten_list():
    t1 = FileInfo(parent="p1", name="n4", size=3, location={"a": "b"})
    t2 = FileInfo(parent="p2", name="n5", size=2, location={"c": "d"})

    vals = t1._flatten_list([t1, t2])
    assert vals == ("p1", "n4", 3, {"a": "b"}, "p2", "n5", 2, {"c": "d"})


@pytest.mark.parametrize("feature_class", [Feature, ShallowFeature])
def test_inheritance(feature_class):
    class SubObject(feature_class):
        subname: str

    class MyTest(feature_class):
        name: str
        sub: SubObject

    class MyTest2(MyTest):
        pass

    with pytest.raises(ValueError):
        MyTest2()

    obj = MyTest2(name="name", sub=SubObject(subname="subname"))
    assert obj._flatten() == ("name", "subname")


def test_naming_transform():
    assert [name for name, _ in MyTest._to_udf_spec()] == [
        "my_test__this_is_name",
        "my_test__sub_class__type",
        "my_test__sub_class__name",
    ]


def test_capital_letter_naming():
    class CAPLetterTEST(Feature):
        AAA_id: str

    vals = [name for name, _ in CAPLetterTEST._to_udf_spec()]
    assert vals == ["cap_letter_test__aaa_id"]


def test_delimiter_in_name():
    with pytest.raises(RuntimeError):

        class MyClass(Feature):
            var__name: str


def test_delimiter_in_name_is_allowed_for_shallow_class():
    class MyClass(ShallowFeature):
        var__name: str

    MyClass._to_udf_spec()

    obj = MyClass(var__name="some stuff")
    dump = obj.model_dump()
    obj._unflatten(dump)


def test_custom_delimiter_in_name():
    with pytest.raises(RuntimeError):

        class MyClass(Feature):
            _delimiter = "EE"
            is_ieee_member: bool


def test_naming_delimiter():
    class MyNestedClassNew(MyNestedClass):
        _delimiter = "+++"

    class MyTestNew(MyTest):
        _delimiter = "+++"

        ThisIsName: str
        subClass: MyNestedClassNew  # noqa: N815

    schema = MyTestNew._to_udf_spec()

    assert [name for name, _ in schema] == [
        "my_test_new+++this_is_name",
        "my_test_new+++sub_class+++type",
        "my_test_new+++sub_class+++name",
    ]


def test_deserialize_nested():
    class Child(Feature):
        type: int
        name: str = Field(default="test1")

    class Parent(Feature):
        name: str
        child: Child

    in_db_map = {
        "parent__name": "a1",
        "parent__child__type": 42,
        "parent__child__name": "a2",
    }

    p = Parent._unflatten(in_db_map)

    assert p.name == "a1"
    assert p.child.type == 42
    assert p.child.name == "a2"


def test_deserialize_shallow():
    class Child(ShallowFeature):
        type: int
        child_name: str = Field(default="test1")

    class Parent(ShallowFeature):
        name: str
        child: Child

    in_db_map = {
        "child_name": "a1",
        "type": 42,
        "name": "a2",
    }

    p = Parent._unflatten(in_db_map)

    assert p.name == "a2"
    assert p.child.type == 42
    assert p.child.child_name == "a1"


def test_deserialize_nested_with_name_normalization():
    class ChildClass(Feature):
        type: int
        name: str = Field(default="test1")

    class Parent(Feature):
        name: str
        childClass11: ChildClass  # noqa: N815

    in_db_map = {
        "parent__name": "name1",
        "parent__child_class11__type": 12,
        "parent__child_class11__name": "n2",
    }

    p = Parent._unflatten(in_db_map)

    assert p.name == "name1"
    assert p.childClass11.type == 12
    assert p.childClass11.name == "n2"


def test_type_array_of_floats():
    class Test1(Feature):
        d: list[float]

    dict_ = {"d": [1, 3, 5]}
    t = Test1(**dict_)
    assert t.d == [1, 3, 5]


def test_class_attr_resolver_basic():
    class MyTest6(Feature):
        val1: list[float]
        pp: int

    assert MyTest6.val1.name == "my_test6__val1"
    assert MyTest6.pp.name == "my_test6__pp"
    assert type(MyTest6.pp.type) == Int
    assert type(MyTest6.val1.type) == Array


def test_class_attr_resolver_shallow():
    class MyTest6(ShallowFeature):
        val1: list[float]
        pp: int

    assert MyTest6.val1.name == "val1"
    assert MyTest6.pp.name == "pp"
    assert type(MyTest6.pp.type) == Int
    assert type(MyTest6.val1.type) == Array


def test_class_attr_resolver_nested():
    assert MyTest.subClass.type.name == "my_test__sub_class__type"
    assert MyTest.subClass.Name.name == "my_test__sub_class__name"
    assert type(MyTest.subClass.type.type) == Int
    assert type(MyTest.subClass.Name.type) == String


def test_class_attr_resolver_nested_3levels():
    class MyTest1(Feature):
        a: int

    class MyTest2(Feature):
        b: MyTest1

    class MyTest3(Feature):
        c: MyTest2

    assert MyTest3.c.b.a.name == "my_test3__c__b__a"
    assert type(MyTest3.c.b.a.type) == Int


def test_list_of_dicts_as_dict():
    class MyTest1(Feature):
        val1: Union[dict, list[dict]]
        val2: Optional[Union[list[dict], dict]]

    schema = Feature._features_to_udf_spec([MyTest1])
    assert len(schema) == 2
    assert next(iter(schema.values())) == JSON
    assert list(schema.values())[1] == JSON


def test_create_column():
    name = "my_col"
    default = "NuLL"

    fr_cls = FeatureTypes.column_class(name, str, default)

    assert issubclass(fr_cls, Feature)
    assert isinstance(fr_cls.my_col, C)
    assert fr_cls.my_col.name == name

    val = "1qa"
    assert fr_cls(my_col=val).my_col == val
    assert fr_cls().my_col == default


def test_create_columns():
    name1 = "cl11"
    name2 = "m234q"

    def1 = "d1wer"
    def2 = 7654

    fr_cls = FeatureTypes.column_classes({name1: (str, def1), name2: (int, def2)})

    assert issubclass(fr_cls, Feature)
    assert isinstance(fr_cls.cl11, C)
    assert isinstance(fr_cls.m234q, C)

    val1 = "deui"
    val2 = 126
    fr = fr_cls(cl11=val1, m234q=val2)
    assert fr.cl11 == val1
    assert fr.m234q == val2

    assert fr_cls().cl11 == def1
    assert fr_cls().m234q == def2


def test_get_value_with_check():
    my_prefix = "111"
    my_suffix = "333"
    def_suffix = "ddd"
    my_value = "22"

    class MyColumn(FeatureTypes.column_class("val", str)):
        def get_value(self, prefix: str, suffix: str = def_suffix) -> str:
            return prefix + super().get_value() + suffix

    fr = MyColumn(val=my_value)

    assert (
        fr._get_value_with_check(my_prefix, my_suffix)
        == my_prefix + my_value + my_suffix
    )
    assert fr._get_value_with_check(my_prefix) == my_prefix + my_value + def_suffix

    with pytest.raises(ValueError):
        fr._get_value_with_check(suffix=my_suffix)

    with pytest.raises(ValueError):
        fr._get_value_with_check()

    assert (
        fr._get_value_with_check(prefix=my_prefix) == my_prefix + my_value + def_suffix
    )


def test_column_class_basic():
    cls = FeatureTypes.column_class("field_name5")
    for type_, value in [
        (str, "val13"),
        (int, 873),
        (dict, {"x": 123, "y": 23.32}),
        (list, ["ee", 34.4, 432]),
    ]:
        obj = cls(field_name5=value)
        assert obj.field_name5 == value
        assert type(obj.field_name5) is type_

    cls_int = FeatureTypes.column_class("field33", int)
    with pytest.raises(ValidationError):
        cls_int(field33="value")

    cls_str = FeatureTypes.column_class("field_76", str)
    with pytest.raises(ValidationError):
        cls_str(field_76=3.14)


def test_column_class_from_sql_column():
    field = "field11"

    for column, value in [
        (C(field, str), "val123"),
        (C(field, int), 463),
        (C(field, float), 1.62),
        (C(field, list), ["a", "b", 33]),
        # No type:
        (C(field), "val123"),
        (C(field), 463),
        (C(field), 1.62),
        (C(field), ["a", "b", 33]),
        # sql type
        (C(field, String), "val123"),
        (C(field, Int), 463),
        (C(field, Float), 1.62),
        (C(field, Array(String)), ["a", "b", 33]),
    ]:
        cls = FeatureTypes.column_class(column)
        obj = cls(field11=value)
        assert obj.field11 == value

    cls_int = FeatureTypes.column_class(C(field, int))
    assert cls_int(field11=123) is not None
    with pytest.raises(ValidationError):
        cls_int(field11="sddsd")
    with pytest.raises(ValidationError):
        cls_int(field11={"ee": "hey"})

    cls_str = FeatureTypes.column_class(C(field, str))
    with pytest.raises(ValidationError):
        cls_str(field11=52)


def test_literal():
    class MyTextBlock(Feature):
        id: int
        type: Literal["text"]

    schema = Feature._features_to_udf_spec([MyTextBlock])
    assert len(schema) == 2
    assert next(iter(schema.values())) == Int
    assert list(schema.values())[1] == String


def test_pydantic_to_feature():
    class MyTextBlock(BaseModel):
        id: int
        type: Literal["text"]

    cls = pydantic_to_feature(MyTextBlock)
    assert Feature.is_feature_class(cls)

    schema = Feature._features_to_udf_spec([cls])
    assert len(schema) == 2
    assert next(iter(schema.values())) == Int
    assert list(schema.values())[1] == String


def test_pydantic_to_feature_nested():
    class MyTextBlock(BaseModel):
        id: int
        type: Literal["text"]

    class MyMessage(BaseModel):
        val1: Optional[str]
        val2: MyTextBlock
        val3: list[MyTextBlock]

    cls = pydantic_to_feature(MyMessage)
    assert Feature.is_feature_class(cls)
    assert Feature.is_feature_class(cls.model_fields["val2"].annotation)
    assert Feature.is_feature_class(get_args(cls.model_fields["val3"].annotation)[0])

    schema = Feature._features_to_udf_spec([cls])
    assert len(schema) == 4
    assert next(iter(schema.values())) == String
    assert list(schema.values())[1] == Int
    assert list(schema.values())[2] == String
    assert type(list(schema.values())[3]) == Array


def test_flatten_schema_with_list_of_objects():
    class FileDir(Feature):
        name: str
        files: list[FileBasic]

    schema = FileDir._to_udf_spec()

    assert len(schema) == 2
    assert [item[0] for item in schema] == ["file_dir__name", "file_dir__files"]

    assert schema[0][1] == String
    assert schema[1][1].to_dict() == {"item_type": {"type": "JSON"}, "type": "Array"}


def test_flatten_schema_with_list_of_ints():
    class SomeInfo(Feature):
        name: str
        vals: list[int]

    schema = SomeInfo._to_udf_spec()

    assert len(schema) == 2
    assert [item[0] for item in schema] == ["some_info__name", "some_info__vals"]

    assert schema[0][1] == String
    assert schema[1][1].to_dict() == {"item_type": {"type": "Int"}, "type": "Array"}
