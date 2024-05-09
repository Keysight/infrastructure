""" Generic clos fabric switch and fabric
"""
from typing import List, Literal, Tuple, Union

if __package__ is None or __package__ == "":
    import generated.infra_pb2 as infra
    import builders as bld
else:
    from .generated import infra_pb2 as infra
    from . import builders as bld


class ClosFabricSwitch(bld.DeviceBuilder):
    name = "Generic fabric switch"
    description = "Generic clos fabric switch"

    def __init__(
        self,
        name: str,
        down_links: int,
        up_links: int,
    ):
        """
        Creates a generic clos fabric switch device

        name: The name of the switch device
        down_links: The number of ports used for down links
        up_links: The number of ports used for up links
        """
        super(ClosFabricSwitch).__init__()
        asic = infra.Component(
            name="asic",
            count=1,
            cpu=infra.Cpu(memory=infra.MemoryType.MEM_RAM),
        )
        self._port_down = infra.Component(
            name="port-down",
            count=down_links,
            nic=infra.Nic(ethernet=infra.Ethernet()),
        )
        mac = infra.Link(
            name="mac",
            type=infra.LinkType.LINK_CUSTOM,
        )
        self._device = infra.Device(
            name=name,
            components={
                asic.name: asic,
                self._port_down.name: self._port_down,
            },
            links={
                mac.name: mac,
            },
        )
        self._create_distributed_intra_package_adjacencies(
            asic,
            mac,
            self._port_down,
        )
        self._port_up = None
        if up_links > 0:
            self._port_up = infra.Component(
                name="port-up",
                count=up_links,
                nic=infra.Nic(ethernet=infra.Ethernet()),
            )
            self.device.components[self._port_up.name].CopyFrom(self._port_up)
            self._create_distributed_intra_package_adjacencies(
                asic,
                mac,
                self._port_up,
            )

    @property
    def port_down_component(self) -> infra.Component:
        return self._port_down

    @property
    def port_up_component(self) -> infra.Component:
        return self._port_up


class ClosFabric(bld.FabricBuilder):
    name: str = "Symmetric Clos Fabric"
    description: str = "Symmetric clos fabric"
    lowest_device: bld.DeviceBuilder = None

    def __init__(
        self,
        host_device: bld.DeviceBuilder,
        host_devices: int = 1,
        rack_capacity: int = 1,
        rack_to_pod_oversubscription: Tuple[int, int] = (1, 1),
        pod_capacity: int = 0,
        pod_to_spine_oversubscription: Tuple[int, int] = (1, 1),
        spine_capacity: int = 0,
    ):
        """Creates an infrastructure of host/rack/pod/spine devices.

        host_device: The host device to be used in the infrastructure
        host_devices: The number of host devices to be represented in the infrastructure
        rack_capacity: The number of host devices per rack switch
            The following are derived from this parameter:
                - the number of downlinks per rack switch
                - the number of rack switches per pod
        rack_to_pod_over_subscription: Tuple(downlink factor, uplink_factor). This parameter determines the number of
            uplinks from rack to pod switches. # of uplinks = (# of downlinks * uplink_factor) / downlink_factor
        pod_capacity: The number of rack switches per pod switch
            The following are derived from this parameters:
                - the number of pod switches
        pod_to_spine_over_subscription: Tuple(downlink factor, uplink_factor) This parameter determines the number of
            uplinks from pod to spine switches. # of uplinks = (# of downlinks * uplink_factor) / downlink_factor
        spine_capacity: The number of pod switches per spine switch
            The following are derived from this parameter:
                - the number of spine switches
        """
        super().__init__(name="clos fabric")
        assert isinstance(host_device, bld.DeviceBuilder)
        assert host_devices >= 1

        self._rack_device, self._rack_devices = self._add_fabric_devices(
            host_device,
            host_devices,
            "rack",
            rack_capacity,
            rack_to_pod_oversubscription,
            pod_capacity,
        )
        self.lowest_device = self._rack_device
        self._pod_device, self._pod_devices = self._add_fabric_devices(
            self._rack_device,
            self._rack_devices,
            "pod",
            pod_capacity,
            pod_to_spine_oversubscription,
            spine_capacity,
        )
        self._spine_device, self._spine_devices = self._add_fabric_devices(
            self._pod_device,
            self._pod_devices,
            "spine",
            spine_capacity,
        )
        device_link = infra.Link(
            name="eth",
            type=infra.LinkType.LINK_ETHERNET,
        )
        self.fabric.links[device_link.name].CopyFrom(device_link)

        # add a connection between rack_device nics and pod_device nics
        if pod_capacity > 0:
            self._add_connection(
                device_link.name,
                self._rack_device,
                self._rack_devices,
                pod_capacity,
                self._pod_device,
                self._pod_devices,
                distribute_connections=True,
            )

    def _add_fabric_devices(
        self,
        lower_device,
        lower_devices,
        device_name,
        lower_capacity,
        over_subscription=(1, 1),
        upper_capacity=None,
    ) -> Tuple[bld.DeviceBuilder, int]:
        """Adds fabric switches to the infrastructure

        Calculates the number of fabric switches and downlinks/uplinks for each
        fabric switch.

        Returns: Tuple of the device and the number of devices
        """
        if lower_capacity == 0:
            return (None, None)
        devices = int(lower_devices / lower_capacity)
        down_links = int(lower_device.port_up_component.count * lower_capacity)
        if upper_capacity == None or upper_capacity == 0:
            up_links = 0
        elif over_subscription[0] > 0 and over_subscription[1] > 0:
            up_links = (down_links * over_subscription[1]) // over_subscription[0]
        else:
            raise ValueError(
                f"Unsupported over subscription value '{over_subscription}', values must be greater than zero"
            )
        device = ClosFabricSwitch(device_name, down_links, up_links)
        self._add_device(device, devices)
        return (device, devices)

    def _add_device(self, package_builder: bld.DeviceBuilder, devices: int) -> None:
        if package_builder is not None:
            self.fabric.devices[package_builder.device.name].CopyFrom(
                infra.DeviceCount(
                    count=devices,
                    device=package_builder.device,
                )
            )

    def _add_connection(
        self,
        link_name: str,
        lower_device: bld.DeviceBuilder,
        lower_number_of_devices: int,
        lower_number_of_devices_per_upper_device: int,
        upper_device: bld.DeviceBuilder,
        upper_number_of_devices: int,
        distribute_connections: bool = False,
    ) -> None:
        """Add a connection that is standard for a clos fabric

        If distribute_connections is false then all connections from one
        device will go to one other device.

        If distribute_connections is true then all connections from the lower
        device will be distributed evenly across all upper devices.
        """
        connections = []
        if isinstance(lower_device, bld.DeviceBuilder) is True:
            c1_component = lower_device.get_nic_component()
        else:
            c1_component = lower_device.port_up_component
        c2_component = upper_device.port_down_component

        if distribute_connections is True and upper_number_of_devices > 1:
            # create a generator for every upper_device component
            def c2_index():
                while True:
                    for i in range(c2_component.count):
                        yield i

            def d2_index():
                while True:
                    for i in range(upper_number_of_devices):
                        yield i

            get_c2_index = []
            for i in range(upper_number_of_devices):
                get_c2_index.append(c2_index())
            get_d2_index = d2_index()
        else:
            # one generator for all upper_device components
            def c2_index():
                while True:
                    for i in range(c2_component.count):
                        yield i

            get_c2_index = c2_index()

        # create connections from lower devices (d1_idx) to upper devices (d2_idx)
        for d1_idx in range(lower_number_of_devices):
            # this is a one-to-one connection from d1_idx -> d2_idx
            d2_idx = int(d1_idx / lower_number_of_devices_per_upper_device)
            for c1_idx in range(c1_component.count):
                if distribute_connections is True and upper_number_of_devices > 1:
                    # this is a distributed connection
                    # one connection from each d1_idx.c1_idx to every d2_idx.c2_idx (round robin)
                    d2_idx = next(get_d2_index)
                    c2_idx = next(get_c2_index[d2_idx])
                else:
                    c2_idx = next(get_c2_index)
                device_link = infra.DeviceLink(
                    d1=lower_device.device.name,
                    d1_index=d1_idx,
                    c1=c1_component.name,
                    c1_index=c1_idx,
                    link=link_name,
                    d2=upper_device.device.name,
                    d2_index=d2_idx,
                    c2=c2_component.name,
                    c2_index=c2_idx,
                )
                connections.append(infra.DeviceConnection(link=device_link))
        self.fabric.connections.extend(connections)
