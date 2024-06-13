from PIL import Image
from torch import Tensor
from torchvision.transforms import ToTensor

from dvcx.lib.file import File
from dvcx.lib.image import ImageReader, convert_image


def test_convert_image(tmp_path):
    file_name = "img.jpg"
    file_path = tmp_path / file_name

    img = Image.new(mode="RGB", size=(64, 64))
    img.save(file_path)

    converted_img = convert_image(
        img,
        mode="RGBA",
        size=(32, 32),
        transform=ToTensor(),
    )
    assert isinstance(converted_img, Tensor)
    assert converted_img.size() == (4, 32, 32)


def test_image_file_reader(tmp_path, catalog, mocker):
    file_name = "img.jpg"
    file_path = tmp_path / file_name

    img = Image.new(mode="RGB", size=(64, 64))
    img.save(file_path)

    kwargs = {
        "mode": "RGBA",
        "size": (32, 32),
        "transform": ToTensor(),
        "open_clip_model": None,
    }
    reader = ImageReader(**kwargs)
    file = File(name=file_name, source=f"file://{tmp_path}")
    file.set_catalog(catalog)

    convert_image = mocker.patch("dvcx.lib.image.convert_image")

    with open(file_path, "rb") as fd:
        file.set_file(fd, caching_enabled=False)
        reader(file.get_value())
        assert len(convert_image.call_args.args) == 1
        assert isinstance(convert_image.call_args.args[0], Image.Image)
        assert convert_image.call_args.kwargs == kwargs
