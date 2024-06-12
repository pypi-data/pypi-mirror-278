import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from random import getrandbits
from typing import ClassVar, Optional, Union

from pydantic import Field, field_validator

from dvcx.cache import UniqueId
from dvcx.client.fileslice import FileSlice
from dvcx.lib.cached_stream import PreCachedStream, PreDownloadStream
from dvcx.lib.feature import ShallowFeature
from dvcx.lib.utils import DvcxError
from dvcx.utils import TIME_ZERO


class FileFeature(ShallowFeature):
    _is_file = True

    def set_file(self, stream, caching_enabled: bool) -> None:
        raise NotImplementedError

    def open(self):
        raise NotImplementedError

    def read(self):
        with self.open() as stream:
            return stream.read()

    def get_value(self):
        return self.read()


class VFileError(DvcxError):
    def __init__(self, file: "File", message: str, vtype: str = ""):
        type_ = f" of vtype '{vtype}'" if vtype else ""
        super().__init__(f"Error in v-file '{file.get_uid().path}'{type_}: {message}")


class VFile(ABC):
    @classmethod
    @abstractmethod
    def get_vtype(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def open(cls, file: "File", location: list[dict]):
        pass


class TarVFile(VFile):
    @classmethod
    def get_vtype(cls) -> str:
        return "tar"

    @classmethod
    def open(cls, file: "File", location: list[dict]):
        if len(location) > 1:
            VFileError(file, "multiple 'location's are not supported yet")

        loc = location[0]

        if (offset := loc.get("offset", None)) is None:
            VFileError(file, "'offset' is not specified")

        if (size := loc.get("size", None)) is None:
            VFileError(file, "'size' is not specified")

        if (parent := loc.get("parent", None)) is None:
            VFileError(file, "'parent' is not specified")

        tar_file = File(**parent)
        tar_file.set_catalog(file._catalog)

        tar_file_uid = tar_file.get_uid()
        client = file._catalog.get_client(tar_file_uid.storage)
        fd = client.open_object(tar_file_uid, use_cache=file._caching_enabled)
        return FileSlice(fd, offset, size, file.name)


class VFileRegistry:
    _vtype_readers: ClassVar[dict[str, type["VFile"]]] = {"tar": TarVFile}

    @classmethod
    def register(cls, reader: type["VFile"]):
        cls._vtype_readers[reader.get_vtype()] = reader

    @classmethod
    def resolve(cls, file: "File", location: list[dict]):
        if len(location) == 0:
            raise VFileError(file, "'location' must not be list of JSONs")

        if not (vtype := location[0].get("vtype", "")):
            raise VFileError(file, "vtype is not specified")

        reader = cls._vtype_readers.get(vtype, None)
        if not reader:
            raise VFileError(file, "reader not registered", vtype)

        return reader.open(file, location)


class File(FileFeature):
    source: str = Field(default="")
    parent: str = Field(default="")
    name: str
    version: str = Field(default="")
    etag: str = Field(default="")
    size: int = Field(default=0)
    vtype: str = Field(default="")
    location: Optional[Union[dict, list[dict]]] = Field(default=None)

    _unique_id_keys: ClassVar[list[str]] = [
        "source",
        "parent",
        "name",
        "etag",
        "size",
        "vtype",
        "location",
    ]

    @staticmethod
    def to_dict(
        v: Optional[Union[str, dict, list[dict]]],
    ) -> Optional[Union[str, dict, list[dict]]]:
        if v is None or v == "":
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception as e:  # noqa: BLE001
                raise ValueError(
                    f"Unable to convert string '{v}' to dict for File feature: {e}"
                ) from None
        return v

    # Workaround for empty JSONs converted to empty strings in some DBs.
    @field_validator("location", mode="before")
    @classmethod
    def validate_location(cls, v):
        return File.to_dict(v)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._stream = None
        self._catalog = None
        self._caching_enabled = False

    def open(self):
        if self.location:
            return VFileRegistry.resolve(self, self.location)

        return self._stream

    def set_catalog(self, catalog):
        self._catalog = catalog

    def set_file(self, stream, caching_enabled: bool) -> None:
        if self._catalog is None:
            raise DvcxError(f"Cannot set file '{stream}' without catalog")

        stream_class = PreCachedStream if caching_enabled else PreDownloadStream
        self._stream = stream_class(stream, self.size, self._catalog, self.get_uid())
        self._caching_enabled = caching_enabled

    def get_uid(self) -> UniqueId:
        dump = self.model_dump()
        return UniqueId(*(dump[k] for k in self._unique_id_keys))

    def get_local_path(self) -> Optional[str]:
        """Get path to a file in a local cache.
        Return None if file is not cached. Throws an exception if cache is not setup."""
        if self._catalog is None:
            raise RuntimeError(
                "cannot resolve local file path because catalog is not setup"
            )
        return self._catalog.cache.get_path(self.get_uid())

    def get_file_suffix(self):
        return Path(self.name).suffix

    def get_file_ext(self):
        return Path(self.name).suffix.strip(".")

    def get_file_stem(self):
        return Path(self.name).stem

    def get_full_name(self):
        if not self.parent:
            return self.name
        return f"{self.parent}/{self.name}"

    def get_full_path(self):
        return f"{self.source}/{self.get_full_name()}"


BinaryFile = File


class TextFile(File):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._file = None

    def set_file(self, stream, caching_enabled: bool) -> None:
        super().set_file(stream, caching_enabled)
        self._stream.set_mode("r")


class FileInfo(FileFeature):
    source: str = Field(default="")
    parent: str = Field(default="")
    name: str
    size: int = Field(default=0)
    location: Optional[Union[dict, list[dict]]] = Field(default=None)
    vtype: str = Field(default="")
    dir_type: int = Field(default=0)
    owner_name: str = Field(default="")
    owner_id: str = Field(default="")
    is_latest: bool = Field(default=True)
    last_modified: datetime = Field(default=TIME_ZERO)
    version: str = Field(default="")
    etag: str = Field(default="")
    random: int = Field(default_factory=lambda: getrandbits(63))

    @field_validator("location", mode="before")
    @classmethod
    def validate_location(cls, v):
        return File.to_dict(v)
