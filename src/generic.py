"""Generic host device
"""
from typing import List, Literal, Type, Tuple

if __package__ is None or __package__ == "":
    import generated.infra_pb2 as infra
    import builders as bld
else:
    from .generated import infra_pb2 as infra
    from . import builders as bld


class GenericHost(bld.HostBuilder):
    """Generic host device that has a one to one relationship between
    npu and nic components.
    """
    name : str  = "Generic host"
    description : str = "Generic host device consisting of an NPU and NIC component"

    def __init__(
        self,
        npu_count=1,
        io_interconnect_bandwidth_gbps: int=0
    ):
        """Creates a generic device with only npu and nic components that are
        connected by a pcie link. 

        Optionally, npu components within a device can be interconnected via generic links attached to a single generic switch.

        name: The name of the generic device
        npu_count: The number of npu/nic components in the device.
        io_interconnect_bandwidth_gbps: npu-to-npu interconnect bandwidth in gigabits per second. If 0, no internal npu-to-npu connectivity will be added to the device.
        """
        super(GenericHost).__init__()
        npu = infra.Component(
            name="npu",
            count=npu_count,
            npu=infra.Npu(),
        )
        self._port_component = infra.Component(
            name="nic",
            count=npu_count,
            nic=infra.Nic(ethernet=infra.Ethernet()),
        )
        pcie = infra.Link(
            name="pcie",
            type=infra.LinkType.LINK_PCIE,
        )
        io_interconnect = infra.Link(
            name="io_interconnect",
            type=infra.LinkType.LINK_CUSTOM,
            bandwidth=infra.Bandwidth(gbps=io_interconnect_bandwidth_gbps),
        )
        io_interconnect_switch = infra.Component(
            name="io_interconnect_switch",
            count=1,
            switch=infra.Switch(custom=infra.Custom()),
        )

        links = { pcie.name: pcie }
        components = {
            npu.name: npu,
            self._port_component.name: self._port_component,
        }
        connections = []
        # Add npu->nic pcie connections
        for npu_idx in range(npu_count):
            connections.append(
                infra.ComponentConnection(
                    link=infra.ComponentLink(
                        c1=npu.name,
                        c1_index=npu_idx,
                        link=pcie.name,
                        c2=self._port_component.name,
                        c2_index=npu_idx,
                    )
                )
            )

        # Add io_interconnect connections if bandwidth was provided
        if io_interconnect_bandwidth_gbps > 0:
            components[io_interconnect_switch.name] = io_interconnect_switch
            links[io_interconnect.name] = io_interconnect
            for npu_idx_a in range(npu_count):
                connections.append(
                    infra.ComponentConnection(
                        link=infra.ComponentLink(
                            c1=npu.name,
                            c1_index=npu_idx_a,
                            link=io_interconnect.name,
                            c2=io_interconnect_switch.name,
                            c2_index=0,
                        )
                    )
                )

        self._device = infra.Device(
            name=self.name,
            components=components,
            links=links,
            connections=connections,
        )

    @property
    def port_up_component(self) -> infra.Component:
        return self._port_component
    
    @property
    def port_down_component(self) -> infra.Component:
        return None

