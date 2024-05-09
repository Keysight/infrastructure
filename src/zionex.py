"""ZionEx package

Uses the infra_pb2 protobuf generated code
to capture components, links, and connections of the
ZionEx block diagram.
"""
from typing import List, Literal, Type, Union

if __package__ is None or __package__ == "":
    import generated.infra_pb2 as infra
    import builders as bld
else:
    from .generated import infra_pb2 as infra
    from . import builders as bld


class ZionEx(bld.HostBuilder):
    """ZionEx package that contains components"""

    name = "ZionEx host device"
    description = "ZionEx host device"

    def __init__(self):
        """Create a ZionEx device consisting of components, links and
        connections.
        """
        super(ZionEx).__init__()
        cpu = infra.Component(name="cpu", count=4, cpu=infra.Cpu())
        oam = infra.Component(name="oam", count=8, npu=infra.Npu())
        self._port_component = infra.Component(name="cc-nic", count=8, nic=infra.Nic())
        emerald_pools_pcie_sw = infra.Component(
            name="ep-sw",
            count=4,
            switch=infra.Switch(pcie=infra.Pcie()),
        )
        clear_creek_pcie_sw = infra.Component(
            name="cc-sw",
            count=4,
            switch=infra.Switch(pcie=infra.Pcie()),
        )
        oam_interconnect = infra.Component(
            name="ep-oam-sw",
            count=1,
            custom=infra.CustomComponent(),
        )
        pciev2 = infra.Link(name="pciev2", type=infra.LinkType.LINK_PCIE)
        pciev3 = infra.Link(name="pciev3", type=infra.LinkType.LINK_PCIE)
        pciev4 = infra.Link(name="pciev4", type=infra.LinkType.LINK_PCIE)
        upi_link = infra.Link(name="upi-link", type=infra.LinkType.LINK_UPI)
        oam_link = infra.Link(name="oam-link", type=infra.LinkType.LINK_NVLINK)
        self._device = infra.Device(
            name="zionex",
            components={
                cpu.name: cpu,
                oam.name: oam,
                self._port_component.name: self._port_component,
                emerald_pools_pcie_sw.name: emerald_pools_pcie_sw,
                clear_creek_pcie_sw.name: clear_creek_pcie_sw,
                oam_interconnect.name: oam_interconnect,
            },
            links={
                upi_link.name: upi_link,
                oam_link.name: oam_link,
                pciev2.name: pciev2,
                pciev3.name: pciev3,
                pciev4.name: pciev4,
            },
        )
        for c1_index in range(cpu.count):
            for c2_index in range(cpu.count):
                if c1_index != c2_index:
                    self._add_component_link(
                        cpu.name,
                        c1_index,
                        upi_link.name,
                        cpu.name,
                        c2_index,
                    )
        for index in range(cpu.count):
            self._add_component_link(
                cpu.name,
                index,
                pciev3.name,
                clear_creek_pcie_sw.name,
                index,
            )
        for index in range(clear_creek_pcie_sw.count):
            self._add_component_link(
                emerald_pools_pcie_sw.name,
                index,
                pciev3.name,
                clear_creek_pcie_sw.name,
                index,
            )
        for c1_index in range(self._port_component.count):
            self._add_component_link(
                self._port_component.name,
                c1_index,
                pciev3.name,
                clear_creek_pcie_sw.name,
                int(c1_index / 2),
            )
        for c1_index in range(oam.count):
            self._add_component_link(
                oam.name,
                c1_index,
                pciev3.name,
                emerald_pools_pcie_sw.name,
                int(c1_index / 2),
            )
        for i in range(oam.count):
            self._add_component_link(
                oam.name,
                i,
                oam_link.name,
                oam_interconnect.name,
                0,
            )

    @property
    def port_up_component(self) -> infra.Component:
        return self._port_component

    @property
    def port_down_component(self) -> infra.Component:
        return None