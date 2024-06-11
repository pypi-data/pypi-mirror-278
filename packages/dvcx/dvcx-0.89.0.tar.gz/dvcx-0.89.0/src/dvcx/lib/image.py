import inspect
from io import BytesIO
from typing import Any, Callable, Optional

try:
    from PIL import Image
except ImportError as exc:
    raise ImportError(
        "Missing dependencies for computer vision:\n"
        "To install run:\n\n"
        "  pip install 'dvcx[cv]'\n"
    ) from exc

from dvcx.lib.file import BinaryFile
from dvcx.lib.reader import FeatureReader


def convert_image(
    img: Image.Image,
    mode: str = "RGB",
    size: Optional[tuple[int, int]] = None,
    transform: Optional[Callable] = None,
    open_clip_model: Optional[Any] = None,
):
    """
    Resize, transform, and otherwise convert an image.

    Args:
        img (Image): PIL.Image object.
        mode (str): PIL.Image mode.
        size (tuple[int, int]): Size in (width, height) pixels for resizing.
        transform (Callable): Torchvision v1 or other transform to apply.
        open_clip_model (Any): Encode image using model from open_clip library.
    """
    if mode:
        img = img.convert(mode)
    if size:
        img = img.resize(size)
    if transform:
        img = transform(img)
        if open_clip_model:
            img = img.unsqueeze(0)  # type: ignore[attr-defined]
    if open_clip_model:
        method_name = "encode_image"
        if not (
            hasattr(open_clip_model, method_name)
            and inspect.ismethod(getattr(open_clip_model, method_name))
        ):
            raise ValueError(
                f"Unable to render Image: 'open_clip_model' doesn't support"
                f" '{method_name}()'"
            )
        img = open_clip_model.encode_image(img)
    return img


class ImageReader(FeatureReader):
    def __init__(
        self,
        mode: str = "RGB",
        size: Optional[tuple[int, int]] = None,
        transform: Optional[Callable] = None,
        open_clip_model: Any = None,
    ):
        """
        Read and optionally transform an image.

        All kwargs are passed to `convert_image()`.
        """
        self.mode = mode
        self.size = size
        self.transform = transform
        self.open_clip_model = open_clip_model
        super().__init__(BinaryFile)

    def __call__(self, value: bytes):
        img = Image.open(BytesIO(value))
        return convert_image(
            img,
            mode=self.mode,
            size=self.size,
            transform=self.transform,
            open_clip_model=self.open_clip_model,
        )
