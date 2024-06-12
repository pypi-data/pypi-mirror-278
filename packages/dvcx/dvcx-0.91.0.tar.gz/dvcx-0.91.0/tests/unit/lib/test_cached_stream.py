import io

from dvcx.lib.cached_stream import ProgressiveCacheStream
from dvcx.lib.file import File

DATA = b"qwertyuiop"
FILE_UID = File(name="name").get_uid()


def test_close(catalog):
    input = io.BytesIO()
    input.write(DATA)
    input.seek(0)

    with ProgressiveCacheStream(input, len(DATA), catalog, FILE_UID) as stream:
        stream.close()
        with open(catalog.cache.get_path(FILE_UID), "rb") as f:
            assert f.read() == DATA


def test_read_by_parts(catalog):
    input = io.BytesIO()
    input.write(DATA)
    input.seek(0)

    with ProgressiveCacheStream(input, len(DATA), catalog, FILE_UID) as stream:
        assert stream.read(1)[0] == DATA[0]
        assert stream.read(5) == DATA[1:6]
        assert stream.read(1)[0] == DATA[6]
        assert stream.read(1024) == DATA[7:]

        stream.close()
        with open(catalog.cache.get_path(FILE_UID), "rb") as f:
            assert f.read() == DATA


def test_seek_forward(catalog):
    input = io.BytesIO()
    input.write(DATA)
    input.seek(0)

    with ProgressiveCacheStream(input, len(DATA), catalog, FILE_UID) as stream:
        stream.seek(4)
        assert stream.read(1)[0] == DATA[4]

        stream.close()
        with open(catalog.cache.get_path(FILE_UID), "rb") as f:
            assert f.read() == DATA


def test_seek_backward(catalog):
    input = io.BytesIO()
    input.write(DATA)
    input.seek(0)

    with ProgressiveCacheStream(input, len(DATA), catalog, FILE_UID) as stream:
        stream.read(8)

        stream.seek(3)
        assert stream.tell() == 3
        assert stream.read(3) == DATA[3:6]

        stream.close()
        with open(catalog.cache.get_path(FILE_UID), "rb") as f:
            assert f.read() == DATA


def test_seek_backward_with_intersection(catalog):
    input = io.BytesIO()
    input.write(DATA)
    input.seek(0)

    with ProgressiveCacheStream(input, len(DATA), catalog, FILE_UID) as stream:
        stream.read(8)

        stream.seek(3)
        assert stream.tell() == 3
        assert stream.read(6) == DATA[3:9]

        stream.close()
        with open(catalog.cache.get_path(FILE_UID), "rb") as f:
            assert f.read() == DATA
