import pandas as pd

from dvcx.lib.feature_udf import FeatureGenerator
from dvcx.lib.file import File, FileInfo


class ParquetGenerator(FeatureGenerator):
    def __init__(self, spec):
        self.spec = spec
        super().__init__(File, [FileInfo, spec])

    def process(self, stream: File):
        with stream.open() as fd:
            df = pd.read_parquet(fd)
        for pq_info, pq_dict in self.parse_parquet(df, stream):
            yield pq_info, self.spec(**pq_dict)

    @staticmethod
    def parse_parquet(df, file_info):
        for idx, pq_dict in enumerate(df.to_dict("records")):
            fstream = FileInfo(
                name=str(idx),
                source=file_info.source,
                parent=file_info.get_full_name(),
                version=file_info.version,
                etag=file_info.etag,
                vtype="parquet",
            )
            yield fstream, pq_dict
