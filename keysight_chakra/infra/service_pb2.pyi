from keysight_chakra.infra import infra_pb2 as _infra_pb2
from keysight_chakra.infra import annotate_pb2 as _annotate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ValidationRequest(_message.Message):
    __slots__ = ("infrastructure", "annotations")
    INFRASTRUCTURE_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    infrastructure: _infra_pb2.Infrastructure
    annotations: _containers.RepeatedCompositeFieldContainer[_annotate_pb2.Annotation]
    def __init__(self, infrastructure: _Optional[_Union[_infra_pb2.Infrastructure, _Mapping]] = ..., annotations: _Optional[_Iterable[_Union[_annotate_pb2.Annotation, _Mapping]]] = ...) -> None: ...

class ValidationError(_message.Message):
    __slots__ = ("optional", "oneof", "map", "referential_integrity", "count")
    OPTIONAL_FIELD_NUMBER: _ClassVar[int]
    ONEOF_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    REFERENTIAL_INTEGRITY_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    optional: str
    oneof: str
    map: str
    referential_integrity: str
    count: str
    def __init__(self, optional: _Optional[str] = ..., oneof: _Optional[str] = ..., map: _Optional[str] = ..., referential_integrity: _Optional[str] = ..., count: _Optional[str] = ...) -> None: ...

class ValidationResponse(_message.Message):
    __slots__ = ("errors", "warnings", "info")
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    errors: _containers.RepeatedCompositeFieldContainer[ValidationError]
    warnings: _containers.RepeatedScalarFieldContainer[str]
    info: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, errors: _Optional[_Iterable[_Union[ValidationError, _Mapping]]] = ..., warnings: _Optional[_Iterable[str]] = ..., info: _Optional[_Iterable[str]] = ...) -> None: ...
