import open_clip
import pytest
import torch

from dvcx.lib.feature_types import FeatureTypes
from dvcx.lib.file import TextFile
from dvcx.lib.text import TextReader, convert_text


@pytest.mark.parametrize("tokenizer_model", ["ViT-B-32", "hf-hub:timm/ViT-B-16-SigLIP"])
def test_convert_text(tmp_path, tokenizer_model):
    text = "thisismytext"
    tokenizer = open_clip.get_tokenizer(tokenizer_model)
    tokenizer_kwargs = {"context_length": 100}
    converted_text = convert_text(
        text, tokenizer=tokenizer, tokenizer_kwargs=tokenizer_kwargs
    )
    assert isinstance(converted_text, torch.Tensor)
    assert converted_text.size() == (100,)


def test_text_reader_column(mocker):
    text = "mytext"
    TextFeature = FeatureTypes.column_class("text")  # noqa: N806
    text_feature = TextFeature(text=text)

    mock_tokenizer = mocker.Mock()
    kwargs = {
        "tokenizer": mock_tokenizer,
        "tokenizer_kwargs": {"some": "arg"},
        "open_clip_model": None,
    }
    reader = TextReader("text", **kwargs)

    convert_text = mocker.patch("dvcx.lib.text.convert_text")
    reader(text_feature.get_value())
    convert_text.assert_called_with(text, **kwargs)


def test_text_reader_file(tmp_path, catalog, mocker):
    file_name = "myfile"
    text = "myText"

    file_path = tmp_path / file_name
    with open(file_path, "w") as fd:
        fd.write(text)

    mock_tokenizer = mocker.Mock()
    kwargs = {
        "tokenizer": mock_tokenizer,
        "tokenizer_kwargs": {"some": "arg"},
        "open_clip_model": None,
    }
    reader = TextReader(**kwargs)
    file = TextFile(name=file_name, source=f"file://{tmp_path}")
    file.set_catalog(catalog)

    convert_text = mocker.patch("dvcx.lib.text.convert_text")
    with open(file_path) as fd:
        file.set_file(fd, caching_enabled=False)
        reader(file.get_value())
        convert_text.assert_called_with(text, **kwargs)
