import pandas as pd

from dvcx.lib.feature import Feature
from dvcx.lib.file import File, FileInfo
from dvcx.lib.parquet import ParquetGenerator


class TestFeature(Feature):
    uid: str
    text: str


def test_parquet_generator(tmp_path, catalog):
    df = pd.DataFrame(
        {
            "uid": ["12345", "67890", "abcde", "f0123"],
            "text": ["28", "22", "we", "hello world"],
        }
    )

    name = "111.parquet"
    pq_path = tmp_path / name
    df.to_parquet(pq_path)
    stream = File(name=name, parent=str(tmp_path))
    stream.set_catalog(catalog)
    with open(pq_path) as fd:
        stream.set_file(fd, caching_enabled=False)
        objs = list(ParquetGenerator(TestFeature).process(stream))

    df_dict = df.to_dict("records")
    assert len(objs) == len(df_dict)
    for ix, (actual, expected) in enumerate(zip(objs, df_dict)):
        file_info, test_feature = actual
        assert type(file_info) == FileInfo
        assert type(test_feature) == TestFeature
        assert test_feature.model_dump() == expected
        assert int(file_info.name) == ix
        assert file_info.vtype == "parquet"
