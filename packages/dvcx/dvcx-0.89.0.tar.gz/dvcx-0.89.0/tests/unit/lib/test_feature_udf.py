import os
from collections.abc import Iterable

import pytest
from pydantic import Field

from dvcx.lib.feature import Feature
from dvcx.lib.feature_udf import (
    FeatureAggregator,
    FeatureBatchMapper,
    FeatureConverter,
    FeatureGenerator,
    FeatureMapper,
    OutputError,
    SchemaError,
    UserCodeError,
)
from dvcx.lib.file import File
from dvcx.query import Stream
from dvcx.query.schema import Column
from dvcx.sql.types import Int


class TestInput(Feature):
    name: str
    parent: str = Field(default="")
    size: int = Field(default=0)


class TestOutput(Feature):
    full_path: str
    size_squared: int = Field(default=0)


class MyAgg(FeatureAggregator):
    def __init__(self):
        super().__init__([TestInput], [TestOutput])

    def process(self, args) -> Iterable[tuple[TestOutput]]:
        row = args[0]
        input = row[0]
        output = TestOutput(
            full_path=os.path.join(input.parent, input.name), size_squared=input.size**2
        )
        yield (output,)


def test_feature_udf_yields_values():
    name = "file.txt"
    path = "dir1/dir2"
    size = 16
    params = ((name, path, size),)

    agg = MyAgg()
    res = list(agg(params))
    assert len(res) == 1

    full_path, size_squared = res[0]
    assert full_path == os.path.join(path, name)
    assert size_squared == size**2


def test_feature_udf_returns_values():
    class MyAggReturn(FeatureAggregator):
        def __init__(self):
            super().__init__([TestInput], [TestOutput])

        def process(self, args):
            row = args[0]
            input = row[0]
            output = TestOutput(
                full_path=os.path.join(input.parent, input.name),
                size_squared=input.size**2,
            )
            return [(output,)]

    name = "f1.txt"
    path = "d1/d2/d55"
    size = 235
    params = ((name, path, size),)

    agg = MyAggReturn()
    res = list(agg(params))
    assert len(res) == 1

    full_path, size_squared = res[0]
    assert full_path == os.path.join(path, name)
    assert size_squared == size**2


class MyAggStream(FeatureAggregator):
    def __init__(self):
        super().__init__([File], [TestOutput])

    def process(self, args):
        output = TestOutput(full_path="xx", size_squared=5)
        yield (output,)


def test_feature_udf_with_stream():
    stream = File(name="tmp.jpg")
    args = ([Stream(), *list(stream._flatten())],)

    agg = MyAggStream()
    res = list(agg(args))
    assert len(res) == 1


def test_feature_udf_with_single_input_and_output():
    class MyAgg(FeatureAggregator):
        def __init__(self):
            super().__init__(TestInput, TestOutput)

        def process(self, args):
            input = args[0]
            output = TestOutput(
                full_path=os.path.join(input.parent, input.name),
                size_squared=input.size**2,
            )
            yield output

    name = "f1.txt"
    path = "dd3"
    size = 343
    params = ((name, path, size),)

    agg = MyAgg()
    res = list(agg(params))
    assert len(res) == 1

    full_path, size_squared = res[0]
    assert full_path == os.path.join(path, name)
    assert size_squared == size**2


def test_incompatible_params_types():
    with pytest.raises(SchemaError):

        class MyAggParamInstance(FeatureAggregator):
            def __init__(self):
                super().__init__(
                    (
                        ("size", Int),
                        ("test", Int),
                    ),
                    TestOutput,
                )

        MyAggParamInstance()

    with pytest.raises(SchemaError):

        class MyAggParamType(FeatureAggregator):
            def __init__(self):
                super().__init__([Int, Int], TestOutput)

        MyAggParamType()

    with pytest.raises(SchemaError):

        class MyAggOutputInstance(FeatureAggregator):
            def __init__(self):
                super().__init__([Int], TestOutput)

        MyAggOutputInstance()


def test_output_length_missmatch_with_params():
    class MyAggWrongLength(FeatureAggregator):
        def __init__(self):
            super().__init__(TestInput, [TestOutput, TestOutput])

        def process(self, args):
            input = args[0]
            output = TestOutput(
                full_path=os.path.join(input.parent, input.name),
                size_squared=input.size**2,
            )
            yield output, output, output

    with pytest.raises(OutputError):
        params = (("file", "dir", 12345),)
        agg = MyAggWrongLength()
        agg(params)


def test_output_type_missmatch_with_params_types():
    class MyAggWrongOutputType(FeatureAggregator):
        def __init__(self):
            super().__init__(TestInput, TestOutput)

        def process(self, args):
            yield 536

    with pytest.raises(OutputError):
        params = (("file", "dir", 12345),)
        agg = MyAggWrongOutputType()
        agg(params)


def test_mapper():
    class MyMap(FeatureMapper):
        def __init__(self):
            super().__init__(TestInput, TestOutput)

        def process(self, test_input):
            return TestOutput(
                full_path=os.path.join(test_input.parent, test_input.name),
                size_squared=test_input.size**2,
            )

    name = "img001.jpg"
    path = "data/dogs"
    size = 56743
    params = (name, path, size)

    agg = MyMap()
    res = agg(*params)

    full_path, size_squared = res
    assert full_path == os.path.join(path, name)
    assert size_squared == size**2


def test_mapper_stream():
    class MyMapStream(FeatureMapper):
        def __init__(self):
            super().__init__([File, TestInput], TestOutput)

        def process(self, inputs):
            stream, test_input = inputs
            return TestOutput(
                full_path=os.path.join(test_input.parent, test_input.name),
                size_squared=test_input.size**2,
            )

    stream = File(name="file.jpg")
    stream_args = (Stream(), *list(stream._flatten()))

    name = "img001.jpg"
    path = "data/dogs"
    size = 56743
    args = (*stream_args, name, path, size)

    agg = MyMapStream()
    res = agg(*args)

    full_path, size_squared = res
    assert full_path == os.path.join(path, name)
    assert size_squared == size**2


def test_batch_mapper():
    class MyBatchMap(FeatureBatchMapper):
        def __init__(self):
            super().__init__(TestInput, TestOutput, 2)

        def process(self, test_inputs):
            for test_input in test_inputs:
                output = TestOutput(
                    full_path=os.path.join(test_input.parent, test_input.name),
                    size_squared=test_input.size**2,
                )
                yield output

    name = "img001.jpg"
    path = "data/dogs"
    size = 56743
    params = ((name, path, size), ("1_" + name, "1_" + path, size * 2))

    agg = MyBatchMap()
    res = agg(params)

    assert len(res) == 2

    full_path, size_squared = res[0]
    assert full_path == os.path.join(path, name)
    assert size_squared == size**2

    full_path, size_squared = res[1]
    assert full_path == os.path.join("1_" + path, "1_" + name)
    assert size_squared == (size * 2) ** 2


def test_generator():
    class MyGen(FeatureGenerator):
        def __init__(self):
            super().__init__(TestInput, TestOutput)

        def process(self, test_input):
            yield TestOutput(
                full_path=os.path.join(test_input.parent, test_input.name) + "_1",
                size_squared=test_input.size**2,
            )

            yield TestOutput(
                full_path=os.path.join(test_input.parent, test_input.name) + "_2",
                size_squared=test_input.size**3,
            )

    name = "img742.jpg"
    path = "d1/cats"
    size = 384
    params = (name, path, size)

    agg = MyGen()
    res = agg(*params)

    assert len(res) == 2

    full_path, size_squared = res[0]
    assert full_path == os.path.join(path, name) + "_1"
    assert size_squared == size**2

    full_path, size_squared = res[1]
    assert full_path == os.path.join(path, name) + "_2"
    assert size_squared == size**3


def test_feature_udf_output_value_instead_of_list():
    class MyAggOutputValueInsteadOfList(FeatureMapper):
        def __init__(self):
            super().__init__([TestInput], [TestOutput])

        def process(self, args):
            input = args[0]
            return TestOutput(
                full_path=os.path.join(input.parent, input.name),
                size_squared=input.size**2,
            )

    name = "file.txt"
    path = "dir1/dir2"
    size = 16
    params = (name, path, size)

    agg = MyAggOutputValueInsteadOfList()
    with pytest.raises(OutputError):
        list(agg(*params))


def test_feature_udf_output_wrong_type():
    class MyAggWrongOutputType(FeatureMapper):
        def __init__(self):
            super().__init__([TestInput], TestOutput)

        def process(self, args):
            return 34

    name = "file.txt"
    path = "dir1/dir2"
    size = 16
    params = (name, path, size)

    agg = MyAggWrongOutputType()
    with pytest.raises(OutputError):
        list(agg(*params))


def test_error_in_user_code():
    class MyBuggyClass(FeatureMapper):
        def __init__(self):
            super().__init__(TestInput, TestOutput)

        def process(self, args):
            return 3.14 / 0

    name = "file.txt"
    path = "dir1/dir2"
    size = 16
    params = (name, path, size)

    agg = MyBuggyClass()
    with pytest.raises(UserCodeError):
        list(agg(*params))


def test_split():
    features = [File]
    f1 = File(name="abc")._flatten()
    f2 = File(name="zxc")._flatten()

    rows = [f1, f2]
    clean_rows, streams = FeatureConverter._separate_streams_from_rows(rows, features)
    assert clean_rows == rows
    assert streams == [None, None]

    rows_with_streams = [(Stream(), *f1), (Stream(), *f2)]
    clean_rows, streams = FeatureConverter._separate_streams_from_rows(
        rows_with_streams, features
    )
    assert clean_rows == rows
    assert len(streams) == 2
    assert isinstance(streams[0], Stream)
    assert isinstance(streams[1], Stream)


def test_feature_like_inputs():
    class FeatureLikeAgg(FeatureAggregator):
        def __init__(self):
            super().__init__(
                [TestInput], [TestOutput.full_path, Column("size_squared"), "ext"]
            )

        def process(self, args) -> Iterable[tuple[str, int, str]]:
            row = args[0]
            input = row[0]
            full_path = os.path.join(input.parent, input.name)
            size_squared = input.size**2
            ext = os.path.splitext(input.name)[1]
            yield (full_path, size_squared, ext)

    name = "file.txt"
    path = "dir1/dir2"
    size = 16
    params = ((name, path, size),)

    agg = FeatureLikeAgg()
    res = list(agg(params))
    assert len(res) == 1

    full_path, size_squared, ext = res[0]
    assert full_path == os.path.join(path, name)
    assert size_squared == size**2
    assert ext == os.path.splitext(name)[1]
