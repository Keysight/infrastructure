from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Data(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: _any_pb2.Any
    def __init__(self, name: _Optional[str] = ..., value: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class Target(_message.Message):
    __slots__ = ("infrastructure", "device", "device_component", "device_component_index", "device_instance", "device_instance_index", "device_instance_index_component", "device_instance_index_component_index")
    INFRASTRUCTURE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_COMPONENT_FIELD_NUMBER: _ClassVar[int]
    DEVICE_COMPONENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    DEVICE_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_INSTANCE_INDEX_FIELD_NUMBER: _ClassVar[int]
    DEVICE_INSTANCE_INDEX_COMPONENT_FIELD_NUMBER: _ClassVar[int]
    DEVICE_INSTANCE_INDEX_COMPONENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    infrastructure: str
    device: str
    device_component: str
    device_component_index: str
    device_instance: str
    device_instance_index: str
    device_instance_index_component: str
    device_instance_index_component_index: str
    def __init__(self, infrastructure: _Optional[str] = ..., device: _Optional[str] = ..., device_component: _Optional[str] = ..., device_component_index: _Optional[str] = ..., device_instance: _Optional[str] = ..., device_instance_index: _Optional[str] = ..., device_instance_index_component: _Optional[str] = ..., device_instance_index_component_index: _Optional[str] = ...) -> None: ...

class Annotation(_message.Message):
    __slots__ = ("targets", "data")
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    targets: _containers.RepeatedCompositeFieldContainer[Target]
    data: Data
    def __init__(self, targets: _Optional[_Iterable[_Union[Target, _Mapping]]] = ..., data: _Optional[_Union[Data, _Mapping]] = ...) -> None: ...
