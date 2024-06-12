import pytest
from torch import Size, Tensor
from torchvision.datasets import FakeData
from torchvision.transforms import v2

from dvcx.catalog import get_catalog
from dvcx.lib.dataset import Dataset
from dvcx.lib.image import ImageReader
from dvcx.lib.pytorch import PytorchDataset
from dvcx.sql.types import Int


@pytest.fixture
def fake_dataset(tmp_path):
    # Create fake images in labeled dirs
    data_path = tmp_path / "data" / ""
    for i, (img, label) in enumerate(FakeData()):
        label = str(label)
        (data_path / label).mkdir(parents=True, exist_ok=True)
        img.save(data_path / label / f"{i}.jpg")

    # Create dataset from images
    uri = data_path.as_uri()
    catalog = get_catalog()

    def extract_label(parent):
        return (int(parent.split("/")[-1]),)

    yield (
        Dataset(uri)
        .map(extract_label, params=("parent",), output={"label": Int})
        .save("fake")
    )

    catalog.remove_dataset("fake", version=1)
    catalog.id_generator.cleanup_for_tests()


def test_pytorch_dataset(tmp_path, fake_dataset):
    transform = v2.Compose([v2.ToTensor(), v2.Resize((64, 64))])
    pt_dataset = PytorchDataset(
        fr_classes=[ImageReader(), "label"],
        name=fake_dataset.name,
        version=fake_dataset.version,
        transform=transform,
    )
    for img, label in pt_dataset:
        assert isinstance(img, Tensor)
        assert isinstance(label, int)
        assert img.size() == Size([3, 64, 64])


def test_pytorch_dataset_sample(fake_dataset):
    transform = v2.Compose([v2.ToTensor(), v2.Resize((64, 64))])
    pt_dataset = PytorchDataset(
        fr_classes=[ImageReader(), "label"],
        name=fake_dataset.name,
        version=fake_dataset.version,
        transform=transform,
        num_samples=700,
    )
    assert len(list(pt_dataset)) == 700


def test_to_pytorch(fake_dataset):
    from torch.utils.data import IterableDataset

    transform = v2.Compose([v2.ToTensor(), v2.Resize((64, 64))])
    pt_dataset = fake_dataset.to_pytorch(ImageReader(), "label", transform=transform)
    assert isinstance(pt_dataset, IterableDataset)
    for img, label in pt_dataset:
        assert isinstance(img, Tensor)
        assert isinstance(label, int)
        assert img.size() == Size([3, 64, 64])
