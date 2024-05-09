"""Generic host device
"""
from typing import List, Literal, Type

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

    def __init__(self, npu_count=1):
        """Creates a generic device with only npu and nic components that are
        connection by a pcie link.

        name: The name of the generic device
        npu_count: The number of npu/nic components in the device.
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
        connections = []
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
        self._device = infra.Device(
            name=self.name,
            components={
                npu.name: npu,
                self._port_component.name: self._port_component,
            },
            links={
                pcie.name: pcie,
            },
            connections=connections,
        )

    @property
    def port_up_component(self) -> infra.Component:
        return self._port_component
    
    @property
    def port_down_component(self) -> infra.Component:
        return None
