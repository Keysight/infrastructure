"""Utility classes for constructing infrastructure

Features:
- extended functionality for finding nodes, building inter-package adjacencies,
  calculating paths etc
"""
from typing import List, Literal, Union, Type, Tuple
from abc import ABC, abstractmethod
import google.protobuf.json_format
import yaml

if __package__ is None or __package__ == "":
    import generated.infra_pb2 as infra
    import utilities.Utilities as Utilities
else:
    from .generated import infra_pb2 as infra
    from .utilities import Utilities


class DeviceBuilder(ABC):
    COMPONENT_TYPES = Literal["cpu", "npu", "nic"]

    def __init__(self):
        self._device: infra.Device = None

    @property
    def device(self) -> infra.Device:
        """Returns the infra_pb2.Device"""
        return self._device

    def serialize(self, type: Literal["yaml", "json", "dict"]) -> Union[str, dict]:
        """Returns the infra_pb2.Device as the specified serialization type"""
        if type == "dict":
            return google.protobuf.json_format.MessageToDict(self._device)
        elif type == "yaml":
            return yaml.dump(google.protobuf.json_format.MessageToDict(self._device))
        elif type == "json":
            return google.protobuf.json_format.MessageToJson(self._device)

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def port_up_component(self) -> infra.Component:
        pass

    @property
    def port_up_component(self) -> infra.Component:
        pass

    def _add_component_link(self, c1, c1_index, link_name, c2, c2_index):
        connection = infra.ComponentConnection(
            link=infra.ComponentLink(
                c1=c1,
                c1_index=c1_index,
                link=link_name,
                c2=c2,
                c2_index=c2_index,
            )
        )
        self._device.connections.extend([connection])

    def _create_distributed_intra_package_adjacencies(
        self,
        c1: infra.Component,
        link: infra.Link,
        c2: infra.Component,
    ):
        """Builds adjacencies

        Ensure max component (c1.count, c2.count) is evenly distributed across
        the min component
        ie c1.count = 16, c2.count = 8
        [0,1] -> [0]
        [2,3] -> [1]
        """
        assert isinstance(c1, infra.Component)
        assert isinstance(link, infra.Link)
        assert isinstance(c2, infra.Component)
        connections = []
        max = c1 if c1.count >= c2.count else c2
        min = c2 if max.name == c1.name else c1
        step = int(max.count / min.count)
        min_idxs = []
        for idx in range(min.count):
            min_idxs.extend([idx] * step)
        cmp_max_min = Utilities.get_indexes(c1, c2)
        for c1_idx, c2_idx in zip(cmp_max_min[0][1], cmp_max_min[1][1]):
            connections.append(
                infra.ComponentConnection(
                    link=infra.ComponentLink(
                        c1=max.name,
                        c1_index=c1_idx,
                        link=link.name,
                        c2=min.name,
                        c2_index=c2_idx,
                    )
                )
            )
        self._device.connections.extend(connections)

    def _create_one_to_one_intra_package_adjacencies(
        self,
        c1: infra.Component,
        link: infra.Link,
        c2: infra.Component,
    ):
        connections = []
        for c1_idx, c2_idx in zip(range(c1.count), range(c2.count)):
            connections.append(
                infra.ComponentConnection(
                    link=infra.ComponentLink(
                        c1=c1.name,
                        c1_index=c1_idx,
                        link=link.name,
                        c2=c2.name,
                        c2_index=c2_idx,
                    )
                )
            )
        self._device.connections.extend(connections)

    def get_nic_component(self) -> infra.Component:
        for component in self._device.components.values():
            if component.HasField("nic") is True:
                return component
        raise Exception(f"Nic component does not exist in package {self._device.name}")

    def get_component(
        self, component_type: COMPONENT_TYPES
    ) -> Union[infra.Component, None]:
        for component in self._device.components.values():
            if component.HasField(component_type) is True:
                return component
        return None

    def get_link(self, link_type: int) -> infra.Link:
        for link in self._device.links:
            if link.type == link_type:
                return link
        raise Exception(
            f"Link type {link_type} does not exist in package {self._device.name}"
        )

    def get_adjacencies(self) -> List[str]:
        adjacencies = []
        for adjacency in self._device.adjacencies:
            adjacencies.append(
                f"{adjacency.c1}.{adjacency.c1_index}.{adjacency.link}.{adjacency.c2}.{adjacency.c2_index}"
            )
        return adjacencies

    def message_to_yaml(self, message) -> str:
        return yaml.dump(
            google.protobuf.json_format.MessageToDict(
                message,
                preserving_proto_field_name=True,
                including_default_value_fields=True,
                use_integers_for_enums=False,
            )
        )

class HostBuilder(DeviceBuilder):
    def __init__(self):
        super(DeviceBuilder).__init__()

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def port_up_component(self) -> infra.Component:
        pass


class FabricBuilder(ABC):
    def __init__(
        self,
        name: str,
        devices: List[Type[infra.Device]] = [],
        links: List[Type[infra.Link]] = [],
    ):
        self._fabric = infra.CustomFabric(
            name=name,
            devices={},
            links={},
            connections=[],
        )
        for package in devices:
            self._fabric.devices[package.name].CopyFrom(package)
        for link in links:
            self._fabric.links[link.name].CopyFrom(link)

    @property
    def fabric(self) -> infra.CustomFabric:
        """Returns: infra_pb2.CustomFabric"""
        return self._fabric

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def lowest_device(self) -> DeviceBuilder:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    def serialize(self, type: Literal["yaml", "json", "dict"]) -> Union[str, dict]:
        """Returns the infra_pb2.Infrastructure as the specified serialization type"""
        if type == "dict":
            return google.protobuf.json_format.MessageToDict(self._fabric)
        elif type == "yaml":
            return yaml.dump(google.protobuf.json_format.MessageToDict(self._fabric))
        elif type == "json":
            return google.protobuf.json_format.MessageToJson(self._fabric)

    def create_one_to_one_adjacencies(
        self,
        pb1: DeviceBuilder,
        component1: int,
        link: infra.Link,
        pb2: DeviceBuilder,
        component2: int,
        mesh: bool = False,
    ):
        assert isinstance(pb1, DeviceBuilder)
        assert isinstance(component1, infra.Component)
        assert isinstance(link, infra.Link)
        assert isinstance(pb2, DeviceBuilder)
        assert isinstance(component2, infra.Component)

        indexes = Utilities.get_adjacency_indexes(
            pb1.package,
            component1,
            pb2.package,
            component2,
            int(pb1.package.count * component1.count / pb2.package.count),
            mesh,
        )
        zipped_indexes = zip(
            indexes["p1"]["indexes"],
            indexes["c1"]["indexes"],
            indexes["p2"]["indexes"],
            indexes["c2"]["indexes"],
        )
        adjacencies = []
        for p1, c1, p2, c2 in zipped_indexes:
            adj = infra.DeviceConnection(
                link=infra.DeviceLink(
                    p1=indexes["p1"]["name"],
                    p1_index=p1,
                    c1=indexes["c1"]["name"],
                    c1_index=c1,
                    link=link.name,
                    p2=indexes["p2"]["name"],
                    p2_index=p2,
                    c2=indexes["c2"]["name"],
                    c2_index=c2,
                )
            )
            adjacencies.append(adj)
        self._fabric.adjacencies.extend(adjacencies)

    def create_inter_package_adjacencies(
        self,
        package1: DeviceBuilder,
        package1_indexes: int,
        component1_indexes: Union[List[int], None],
        package2: DeviceBuilder,
        package2_indexes: int,
        component2_indexes: Union[List[int], None],
        link: infra.LinkType,
    ):
        """
        Builds inter-package adjacencies between two package components.

        Parameters
        ----------
        p1: source package
        component_type: source component type
        c2_type: Destination component
        link: Link between c1 and c2
        c1_indexes: The indexes of the c1 components that will be used when
            creating adjacencies. If None then the entire count of the component
            will be used.
        """
        assert len(component1_indexes) == len(component2_indexes)
        adjacencies = []
        c1 = package1.get_nic_component()
        c2 = package2.get_nic_component()
        for p1_index, p2_index in zip(package1_indexes, package2_indexes):
            for c1_index, c2_index in zip(component1_indexes, component2_indexes):
                adj = infra.DeviceConnection(
                    link=infra.DeviceConnection(
                        p1=package1.package.name,
                        p1_index=p1_index,
                        c1=c1.name,
                        c1_index=c1_index,
                        link=link.name,
                        p2=package2.package.name,
                        p2_index=p2_index,
                        c2=c2.name,
                        c2_index=c2_index,
                    )
                )
                adjacencies.append(adj)
        self._fabric.adjacencies.extend(adjacencies)

    def create_many_to_many_inter_package_adjacencies(
        self,
        package1: DeviceBuilder,
        package2: DeviceBuilder,
        link: infra.LinkType,
        index_pairs: List[Tuple[List[int], List[int]]],
    ):
        """
        Builds inter-package adjacencies between two package components.

        Need to be able to handle the following type of use case:

        pkg1[0].cmp1[0,1].link.pkg2[0].cmp2[0,1]
        pkg1[0].cmp1[2,3].link.pkg2[1].cmp2[0,1]
        pkg1[1].cmp1[0,1].link.pkg2[1].cmp2[2,3]
        pkg1[1].cmp1[2,3].link.pkg2[0].cmp2[0,1]

        need something like this:
        list[tuple(tuple(list[int], list[int]), tuple(list[int], list[int]))]

        Parameters
        ----------
        src_dst_index_pairs: A list of src/dst index pairs. Each index pair
        """
        adjacencies = []
        component1 = package1.get_nic_component()
        component2 = package2.get_nic_component()
        for src_idxs, dst_idxs in index_pairs:
            for pkg1_idx, pkg2_idx in zip(src_idxs[0], dst_idxs[0]):
                for cmp1_idx, cmp2_idx in zip(src_idxs[1], dst_idxs[1]):
                    adjacencies.append(
                        infra.DeviceConnection(
                            link=infra.DeviceLink(
                                p1=package1.package.name,
                                p1_index=pkg1_idx,
                                c1=component1.name,
                                c1_index=cmp1_idx,
                                link=link.name,
                                p2=package2.package.name,
                                p2_index=pkg2_idx,
                                c2=component2.name,
                                c2_index=cmp2_idx,
                            )
                        )
                    )
        self._fabric.adjacencies.extend(adjacencies)

    def get_link(self, link_type: int) -> infra.Link:
        for link in self._fabric.links:
            if link.type == link_type:
                return link
        raise Exception(
            f"Inter package link of type {link_type} does not exist in system {self._fabric.name}"
        )

class InfraBuilder(ABC):
    def __init__(
        self,
        fabric: infra.CustomFabric = infra.CustomFabric(),
        hosts: infra.Hosts = infra.Hosts(),
        connections: List[Type[infra.DeviceConnection]] = [],
        links: List[Type[infra.Link]] = [],
    ):
        self._infra = infra.Infrastructure(
            custom_fabric=fabric,
            hosts=hosts,
            connections=connections,
            links={}
        )

        for link in links:
            self._infra.links[link.name].CopyFrom(link)

    @property
    def infrastructure(self) -> infra.Infrastructure:
        """Returns: infra_pb2.Infrastructure"""
        return self._infra

    def serialize(self, type: Literal["yaml", "json", "dict"]) -> Union[str, dict]:
        """Returns the infra_pb2.Infrastructure as the specified serialization type"""
        if type == "dict":
            return google.protobuf.json_format.MessageToDict(self._infra)
        elif type == "yaml":
            return yaml.dump(google.protobuf.json_format.MessageToDict(self._infra))
        elif type == "json":
            return google.protobuf.json_format.MessageToJson(self._infra)
