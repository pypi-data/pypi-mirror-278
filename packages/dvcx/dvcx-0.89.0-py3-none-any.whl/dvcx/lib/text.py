import inspect
from typing import TYPE_CHECKING, Any, Callable, Optional

from dvcx.lib.file import TextFile
from dvcx.lib.reader import FeatureReader

if TYPE_CHECKING:
    from dvcx.lib.feature_types import FeatureLike


def convert_text(
    text: str,
    tokenizer: Optional[Callable] = None,
    tokenizer_kwargs: Optional[dict[str, Any]] = None,
    open_clip_model: Optional[Any] = None,
):
    """
    Tokenize and otherwise transform text.

    Args:
        text (str): Text to convert.
        tokenizer (Callable): Tokenizer to use to tokenize objects.
        tokenizer_kwargs (dict): Additional kwargs to pass when calling tokenizer.
        open_clip_model (Any): Encode text using model from open_clip library.
    """
    if open_clip_model:
        method_name = "encode_text"
        if not (
            hasattr(open_clip_model, method_name)
            and inspect.ismethod(getattr(open_clip_model, method_name))
        ):
            raise ValueError(
                f"TextColumn error: 'model' doesn't support '{method_name}()'"
            )

    if not tokenizer:
        return text

    if tokenizer_kwargs:
        res = tokenizer([text], **tokenizer_kwargs)
    else:
        res = tokenizer([text])
    from transformers.tokenization_utils_base import PreTrainedTokenizerBase

    tokens = (
        res.input_ids[0] if isinstance(tokenizer, PreTrainedTokenizerBase) else res[0]
    )
    if not open_clip_model:
        return tokens

    return open_clip_model.encode_text(tokens.unsqueeze(0))


class TextReader(FeatureReader):
    def __init__(
        self,
        fr_class: "FeatureLike" = TextFile,
        tokenizer: Optional[Callable] = None,
        tokenizer_kwargs: Optional[dict[str, Any]] = None,
        open_clip_model: Optional[Any] = None,
    ):
        """
        Read and optionally transform a text column.

        All kwargs are passed to `convert_text()`.
        """
        self.tokenizer = tokenizer
        self.tokenizer_kwargs = tokenizer_kwargs
        self.open_clip_model = open_clip_model
        super().__init__(fr_class)

    def __call__(self, value: str):
        return convert_text(
            value,
            tokenizer=self.tokenizer,
            tokenizer_kwargs=self.tokenizer_kwargs,
            open_clip_model=self.open_clip_model,
        )
