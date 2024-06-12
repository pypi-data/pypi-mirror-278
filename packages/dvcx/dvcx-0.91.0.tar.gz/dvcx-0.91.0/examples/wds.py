import pandas as pd

from dvcx.lib.dataset import C, Dataset
from dvcx.lib.parquet import ParquetGenerator
from dvcx.lib.webdataset import WebDataset
from dvcx.lib.webdataset_laion import WDSLaion
from dvcx.lib.webdataset_meta import LaionParquet

wds = (
    Dataset("gcs://dvcx-datacomp-small/shards")
    .filter(C.name.glob("00000000.tar"))
    .generate(WebDataset(spec=WDSLaion), cache=True)
)

meta = (
    Dataset("gcs://dvcx-datacomp-small/metadata")
    .filter(C.name.glob("0020f*.parquet"))
    .generate(ParquetGenerator(LaionParquet), cache=True)
    .select(LaionParquet)
)

res = wds.merge(meta, on=WDSLaion.json.uid, right_on=LaionParquet.uid)

df = res.limit(10).to_pandas()
with pd.option_context("display.max_columns", None):
    print(df)
