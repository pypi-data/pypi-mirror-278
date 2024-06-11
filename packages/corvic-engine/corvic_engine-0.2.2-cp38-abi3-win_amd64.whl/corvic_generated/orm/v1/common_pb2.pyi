from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BlobUrlList(_message.Message):
    __slots__ = ("blob_urls",)
    BLOB_URLS_FIELD_NUMBER: _ClassVar[int]
    blob_urls: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, blob_urls: _Optional[_Iterable[str]] = ...) -> None: ...
