from com.terraquantum.storage.v1alpha1 import storage_pb2 as _storage_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StorageTransferRequestedProto(_message.Message):
    __slots__ = ("id", "url", "project_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    url: str
    project_id: str
    def __init__(self, id: _Optional[str] = ..., url: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...

class StorageCreatedProto(_message.Message):
    __slots__ = ("id", "project_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...

class StorageStatusChangedProto(_message.Message):
    __slots__ = ("id", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: _storage_pb2.StorageStatusProto
    def __init__(self, id: _Optional[str] = ..., status: _Optional[_Union[_storage_pb2.StorageStatusProto, str]] = ...) -> None: ...

class StorageDeletionRequestedProto(_message.Message):
    __slots__ = ("id", "project_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...
