import open_clip
import torch
from torch.nn.functional import cosine_similarity
from torch.utils.data import DataLoader

from dvcx.lib.dataset import C, Dataset
from dvcx.lib.feature_udf import FeatureMapper
from dvcx.lib.file import TextFile
from dvcx.lib.image import ImageReader
from dvcx.lib.text import TextReader
from dvcx.sql.functions import path

source = "gcs://dvcx-50k-laion-files/000000/00000000*"


class CaptionMapper(FeatureMapper):
    def process(self, data: TextFile) -> str:
        return data.get_value()


def create_dataset():
    imgs = (
        Dataset(source).filter(C.name.glob("*.jpg")).mutate(stem=path.file_stem(C.name))
    )
    captions = (
        Dataset(source)
        .filter(C.name.glob("*.txt"))
        .mutate(stem=path.file_stem(C.name))
        .map(CaptionMapper(TextFile, "caption"))
    )
    return imgs.join(captions.select("stem", "caption"), "stem").save("laion-50k")


if __name__ == "__main__":
    q = create_dataset()

    model, _, preprocess = open_clip.create_model_and_transforms(
        "ViT-B-32", pretrained="laion2b_s34b_b79k"
    )
    tokenizer = open_clip.get_tokenizer("ViT-B-32")

    ds = q.to_pytorch(
        ImageReader(transform=preprocess),
        TextReader("caption", tokenizer=tokenizer),
    )
    loader = DataLoader(ds, batch_size=16)

    similarity_sum = 0
    row_count = 0
    with torch.no_grad(), torch.cuda.amp.autocast():
        for image, text in loader:
            image_features = model.encode_image(image)
            text_features = model.encode_text(text)
            similarity_sum += (
                cosine_similarity(image_features, text_features).sum().item()
            )
            row_count += len(image_features)

    print("Average cosine similarity:", similarity_sum / row_count)
