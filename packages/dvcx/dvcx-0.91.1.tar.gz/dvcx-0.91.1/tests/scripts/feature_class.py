from dvcx.lib.dataset import C, Dataset
from dvcx.lib.feature import ShallowFeature
from dvcx.lib.feature_udf import FeatureMapper
from dvcx.lib.file import BinaryFile


class Embedding(ShallowFeature):
    emb: float


class EmbeddingMapper(FeatureMapper):
    def process(self, data):
        return Embedding(emb=512)


ds_name = "feature_class"
ds = (
    Dataset(path="gcs://dvcx-datalakes/dogs-and-cats/")
    .filter(C.name.glob("*cat*.jpg"))  # type: ignore [attr-defined]
    .limit(5)
)
ds.map(EmbeddingMapper(inputs=BinaryFile, outputs=Embedding)).save(ds_name)
