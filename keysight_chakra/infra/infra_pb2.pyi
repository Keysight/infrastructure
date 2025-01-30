from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemoryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEM_UNSPECIFIED: _ClassVar[MemoryType]
    MEM_RAM: _ClassVar[MemoryType]
    MEM_HBM: _ClassVar[MemoryType]
    MEM_CXL: _ClassVar[MemoryType]
MEM_UNSPECIFIED: MemoryType
MEM_RAM: MemoryType
MEM_HBM: MemoryType
MEM_CXL: MemoryType

class CustomComponent(_message.Message):
    __slots__ = ("memory",)
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    memory: MemoryType
    def __init__(self, memory: _Optional[_Union[MemoryType, str]] = ...) -> None: ...

class Npu(_message.Message):
    __slots__ = ("memory",)
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    memory: MemoryType
    def __init__(self, memory: _Optional[_Union[MemoryType, str]] = ...) -> None: ...

class Cpu(_message.Message):
    __slots__ = ("memory",)
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    memory: MemoryType
    def __init__(self, memory: _Optional[_Union[MemoryType, str]] = ...) -> None: ...

class Infiniband(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Ethernet(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Nic(_message.Message):
    __slots__ = ("ethernet", "infinband")
    ETHERNET_FIELD_NUMBER: _ClassVar[int]
    INFINBAND_FIELD_NUMBER: _ClassVar[int]
    ethernet: Ethernet
    infinband: Infiniband
    def __init__(self, ethernet: _Optional[_Union[Ethernet, _Mapping]] = ..., infinband: _Optional[_Union[Infiniband, _Mapping]] = ...) -> None: ...

class Pcie(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NvLink(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Custom(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Switch(_message.Message):
    __slots__ = ("pcie", "nvswitch", "custom")
    PCIE_FIELD_NUMBER: _ClassVar[int]
    NVSWITCH_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    pcie: Pcie
    nvswitch: NvLink
    custom: Custom
    def __init__(self, pcie: _Optional[_Union[Pcie, _Mapping]] = ..., nvswitch: _Optional[_Union[NvLink, _Mapping]] = ..., custom: _Optional[_Union[Custom, _Mapping]] = ...) -> None: ...

class Component(_message.Message):
    __slots__ = ("name", "count", "custom", "cpu", "npu", "nic", "switch")
    NAME_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    NPU_FIELD_NUMBER: _ClassVar[int]
    NIC_FIELD_NUMBER: _ClassVar[int]
    SWITCH_FIELD_NUMBER: _ClassVar[int]
    name: str
    count: int
    custom: CustomComponent
    cpu: Cpu
    npu: Npu
    nic: Nic
    switch: Switch
    def __init__(self, name: _Optional[str] = ..., count: _Optional[int] = ..., custom: _Optional[_Union[CustomComponent, _Mapping]] = ..., cpu: _Optional[_Union[Cpu, _Mapping]] = ..., npu: _Optional[_Union[Npu, _Mapping]] = ..., nic: _Optional[_Union[Nic, _Mapping]] = ..., switch: _Optional[_Union[Switch, _Mapping]] = ...) -> None: ...

class Bandwidth(_message.Message):
    __slots__ = ("gbps", "gBs", "gts")
    GBPS_FIELD_NUMBER: _ClassVar[int]
    GBS_FIELD_NUMBER: _ClassVar[int]
    GTS_FIELD_NUMBER: _ClassVar[int]
    gbps: int
    gBs: int
    gts: int
    def __init__(self, gbps: _Optional[int] = ..., gBs: _Optional[int] = ..., gts: _Optional[int] = ...) -> None: ...

class Link(_message.Message):
    __slots__ = ("name", "description", "bandwidth")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    BANDWIDTH_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    bandwidth: Bandwidth
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., bandwidth: _Optional[_Union[Bandwidth, _Mapping]] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ("name", "components", "links", "connections")
    class ComponentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Component
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Component, _Mapping]] = ...) -> None: ...
    class LinksEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Link
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Link, _Mapping]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    components: _containers.MessageMap[str, Component]
    links: _containers.MessageMap[str, Link]
    connections: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., components: _Optional[_Mapping[str, Component]] = ..., links: _Optional[_Mapping[str, Link]] = ..., connections: _Optional[_Iterable[str]] = ...) -> None: ...

class DeviceInstances(_message.Message):
    __slots__ = ("name", "device", "count")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    name: str
    device: str
    count: int
    def __init__(self, name: _Optional[str] = ..., device: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class Inventory(_message.Message):
    __slots__ = ("devices", "links")
    class DevicesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Device
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Device, _Mapping]] = ...) -> None: ...
    class LinksEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Link
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Link, _Mapping]] = ...) -> None: ...
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.MessageMap[str, Device]
    links: _containers.MessageMap[str, Link]
    def __init__(self, devices: _Optional[_Mapping[str, Device]] = ..., links: _Optional[_Mapping[str, Link]] = ...) -> None: ...

class Infrastructure(_message.Message):
    __slots__ = ("inventory", "device_instances", "connections")
    class DeviceInstancesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: DeviceInstances
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[DeviceInstances, _Mapping]] = ...) -> None: ...
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    DEVICE_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    inventory: Inventory
    device_instances: _containers.MessageMap[str, DeviceInstances]
    connections: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, inventory: _Optional[_Union[Inventory, _Mapping]] = ..., device_instances: _Optional[_Mapping[str, DeviceInstances]] = ..., connections: _Optional[_Iterable[str]] = ...) -> None: ...
