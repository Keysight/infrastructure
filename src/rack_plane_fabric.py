"""RackPlaneFabric package

Uses the infra_pb2 protobuf generated code
to capture components, links, and connections of the
RackPlane block diagram.
"""

from typing import Tuple

if __package__ is None or __package__ == "":
    import generated.infra_pb2 as infra
    import builders as bld
    from keysight_chakra.closfabric import ClosFabricSwitch
else:
    from .generated import infra_pb2 as infra
    from . import builders as bld
    from .closfabric import ClosFabricSwitch


class RackPlaneFabricBuilder(bld.FabricBuilder):
    """
    generates infrastructure of a fabric that
    supports connecting to switching via multiple planes
    """

    name: str = "RackPlaneFabric"
    description: str = "fabric that users multiple planes inside a rack"
    lowest_device: bld.DeviceBuilder = None

    def __init__(self, host_builder: bld.DeviceBuilder, host_count: int = 1):
        super().__init__(self.name)
        assert isinstance(host_builder, bld.DeviceBuilder)

        rack_switch, _ = self._add_fabric_devices(
            host_builder,
            host_count,
            "RackSwitch",
        )
        self.lowest_device = rack_switch

        device_link = infra.Link(
            name="eth",
            type=infra.LinkType.LINK_ETHERNET,
        )
        self.fabric.links[device_link.name].CopyFrom(device_link)

    def _add_fabric_devices(
        self,
        host_builder: bld.DeviceBuilder,
        host_count: int,
        device_name: str,
    ) -> Tuple[bld.DeviceBuilder, int]:
        """Adds fabric switches to the infrastructure
        Returns: Tuple of the device and the number of devices
        """
        down_link_count = int(host_builder.port_up_component.count * host_count)
        up_link_count = 0
        device = ClosFabricSwitch(device_name, down_link_count, up_link_count)
        # create one rack switch per host scale up nic
        sw_count = host_builder.port_up_component.count
        self._add_device(device, sw_count)
        return (device, sw_count)

    def _add_device(
        self, package_builder: bld.DeviceBuilder, device_count: int
    ) -> None:
        if package_builder is not None:
            self.fabric.devices[package_builder.device.name].CopyFrom(
                infra.DeviceCount(
                    count=device_count,
                    device=package_builder.device,
                )
            )
