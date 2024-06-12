import io
import json

import pytest

from dvcx.cache import UniqueId
from dvcx.catalog import Catalog
from dvcx.lib.file import File, FileInfo, TextFile
from dvcx.lib.utils import DvcxError


def test_uid_missing_location():
    name = "my_name"
    vtype = "vt1"

    stream = File(name=name, vtype=vtype)
    assert stream.get_uid() == UniqueId("", "", name, "", 0, vtype, None)


def test_uid_location():
    name = "na_me"
    vtype = "some_random"
    loc = {"e": 42}

    stream = File(name=name, vtype=vtype, location=loc)
    assert stream.get_uid() == UniqueId("", "", name, "", 0, vtype, loc)


def test_file_stem():
    s = File(name=".file.jpg.txt")
    assert s.get_file_stem() == ".file.jpg"


def test_file_ext():
    s = File(name=".file.jpg.txt")
    assert s.get_file_ext() == "txt"


def test_file_suffix():
    s = File(name=".file.jpg.txt")
    assert s.get_file_suffix() == ".txt"


def test_full_name():
    name = ".file.jpg.txt"
    f = File(name=name)
    assert f.get_full_name() == name

    parent = "dir1/dir2"
    f = File(name=name, parent=parent)
    assert f.get_full_name() == f"{parent}/{name}"


def test_cache_get_path(catalog: Catalog):
    stream = File(name="test.txt1", source="s3://mybkt")
    stream.set_catalog(catalog)

    uid = stream.get_uid()
    data = b"some data is heRe"
    catalog.cache.store_data(uid, data)

    path = stream.get_local_path()
    assert path is not None

    with open(path, mode="rb") as f:
        assert f.read() == data


def test_read_binary_data(tmp_path, catalog: Catalog):
    file_name = "myfile"
    data = b"some\x00data\x00is\x48\x65\x6c\x57\x6f\x72\x6c\x64\xff\xffheRe"

    file_path = tmp_path / file_name
    with open(file_path, "wb") as fd:
        fd.write(data)

    file = File(name=file_name, source=f"file://{tmp_path}")
    file.set_catalog(catalog)

    with open(file_path, "rb") as fd:
        file.set_file(fd, caching_enabled=False)
        assert file.read() == data


def test_read_binary_data_as_text(tmp_path, catalog: Catalog):
    file_name = "myfile43.txt"
    data = b"some\x00data\x00is\x48\x65\x6c\x57\x6f\x72\x6c\x64\xff\xffheRe"

    file_path = tmp_path / file_name
    with open(file_path, "wb") as fd:
        fd.write(data)

    file = TextFile(name=file_name, source=f"file://{tmp_path}")
    file.set_catalog(catalog)

    with open(file_path) as fd:
        file.set_file(fd, caching_enabled=False)
        try:
            x = file.read()
        except UnicodeDecodeError:  # Unix
            pass
        else:  # Windows
            assert x != data


def test_read_text_data(tmp_path, catalog: Catalog):
    file_name = "myfile"
    data = "this is a TexT data..."

    file_path = tmp_path / file_name
    with open(file_path, "w") as fd:
        fd.write(data)

    file = TextFile(name=file_name, source=f"file://{tmp_path}")
    file.set_catalog(catalog)

    with open(file_path) as fd:
        file.set_file(fd, caching_enabled=False)
        assert file.read() == data


def test_set_file_no_catalog(catalog):
    stream = File(name="name33")
    with pytest.raises(DvcxError):
        stream.set_file(io.StringIO(), False)


def test_cache_get_path_without_cache():
    stream = File(name="test.txt1", source="s3://mybkt")
    with pytest.raises(RuntimeError):
        stream.get_local_path()


def test_json_from_string():
    d = {"e": 12}

    file = File(name="something", location=d)
    assert file.location == d

    file = File(name="something", location=None)
    assert file.location is None

    file = File(name="something", location="")
    assert file.location is None

    file = File(name="something", location=json.dumps(d))
    assert file.location == d

    with pytest.raises(ValueError):
        File(name="something", location="{not a json}")


def test_file_info_jsons():
    file = FileInfo(name="something", location="")
    assert file.location is None

    d = {"e": 12}
    file = FileInfo(name="something", location=json.dumps(d))
    assert file.location == d
