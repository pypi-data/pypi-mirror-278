from __future__ import annotations

import contextlib
import gzip
import sys
from io import BytesIO
from pathlib import Path
from typing import Optional, Any, List, IO, Iterable, Union

import msgpack

from .base import wrap, TypeMatcher, DictAdapter, AbstractAdapter

__version__ = "0.2.0"
format_version: int = 1

# Should never be changed
INTRODUCTION_PHRASE = "unpack me with antipickle"


class AntipickleConfig:
    MAX_BUFFER_SIZE: int = 10 * 1024**3  # 10 GB by default


# required by .isoformat in python's datetime
assert sys.version_info >= (3, 7), "Old python is not supported by antipickle"


class AntipickleSerializationError(RuntimeError):
    pass


class AntipickleDeserializationError(RuntimeError):
    pass


def get_matcher(adapters: Optional[list]) -> TypeMatcher:
    from .adapters_default import all_default_adapters

    matcher = TypeMatcher()
    matcher.register_adapter(DictAdapter())
    if adapters is not None:
        for c in adapters:
            matcher.register_adapter(c)
    for c in all_default_adapters:
        matcher.register_adapter(c)
    return matcher


class Packer:
    def __init__(self, f: IO[bytes], *, adapters: Optional[List[AbstractAdapter]] = None):
        self.f = f
        self.matcher = get_matcher(adapters)
        metadata = None
        self.f.write(msgpack.packb([INTRODUCTION_PHRASE, format_version, metadata]))

    def add(self, obj: Any):
        self.f.write(msgpack.packb(wrap(obj), default=self.matcher.serialize_helper))


def load_sequence(f: IO[bytes], *, adapters: Optional[List[AbstractAdapter]] = None) -> Iterable[Any]:
    matcher = get_matcher(adapters=adapters)
    unpacker = msgpack.Unpacker(
        f,
        object_hook=matcher.deserialize_helper,
        max_buffer_size=AntipickleConfig.MAX_BUFFER_SIZE,
    )
    intro = next(unpacker)
    if (
        not isinstance(intro, list)
        or len(intro) != 3
        or intro[0] != INTRODUCTION_PHRASE
        or not isinstance(intro[1], int)
    ):
        raise AntipickleDeserializationError("Wrong format or corrupted file")
    if intro[1] > format_version:
        raise AntipickleDeserializationError(f"Antipickle format {format_version} not supported; update antipickle")
    yield from unpacker


def dump_sequence(
    sequence: Iterable[Any],
    f: IO[bytes],
    *,
    adapters: Optional[List[AbstractAdapter]] = None,
):
    packer = Packer(f, adapters=adapters)
    for x in sequence:
        packer.add(x)


@contextlib.contextmanager
def get_file_handle(filename: str, mode: str):
    assert mode in ("rb", "wb")
    use_fsspec = "://" in filename
    if not use_fsspec:
        handle = open(filename, mode=mode)
    else:
        import fsspec

        handle = fsspec.open(filename, mode=mode)

    if filename.endswith(".gz"):
        with handle as fraw:
            with gzip.open(fraw, mode=mode) as f:
                yield f
    else:
        with handle as f:
            yield f


def dump(
    obj: Any,
    filename: Union[str, Path],
    *,
    adapters: Optional[List[AbstractAdapter]] = None,
):
    assert isinstance(filename, (str, Path)), f"Passed filename is of a wrong type: {type(filename)}"
    filename = str(filename)
    assert len(filename) < 1000, "Filename is too long, check order of arguments"
    with get_file_handle(filename, mode="wb") as f:
        dump_sequence([obj], f, adapters=adapters)


def load(filename: Union[str, Path], *, adapters: Optional[List[AbstractAdapter]] = None) -> Any:
    assert isinstance(filename, (str, Path)), f"Passed filename is of a wrong type {type(filename)}"
    filename = str(filename)
    with get_file_handle(filename, mode="rb") as f:
        loaded = list(load_sequence(f, adapters=adapters))

    if len(loaded) == 0:
        raise AntipickleDeserializationError("File is empty")
    if len(loaded) != 1:
        raise AntipickleDeserializationError("More than one object is stored, use antipickle.load_sequence")
    return loaded[0]


def dumps(obj: Any, *, adapters: Optional[List[AbstractAdapter]] = None) -> bytes:
    b = BytesIO()
    dump_sequence([obj], f=b, adapters=adapters)
    return b.getvalue()


def loads(b: bytes, *, adapters: Optional[List[AbstractAdapter]] = None) -> Any:
    loaded = list(load_sequence(BytesIO(b), adapters=adapters))
    if len(loaded) == 0:
        raise AntipickleDeserializationError("File is empty")
    if len(loaded) != 1:
        raise AntipickleDeserializationError("More than one object is stored, use antipickle.load_sequence")
    return loaded[0]
