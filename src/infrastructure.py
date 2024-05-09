""" Generic infrastructure
"""
from typing import List, Literal, Tuple, Union

if __package__ is None or __package__ == "":
    import generated.infra_pb2 as infra
    import builders as bld
else:
    from .generated import infra_pb2 as infra
    from . import builders as bld

class Infrastructure(bld.InfraBuilder):
    name: str = "Generic Infrastructure"
    description: str = "Generic Infrastructure"

    def __init__(
        self,
        host_device: bld.DeviceBuilder,
        host_devices: int = 1,
        fabric: bld.FabricBuilder = None,
        assignment_scheme: Literal["NONE", "ROUND_ROBIN", "ONE_TO_ONE"] = "NONE"
    ):
        """Creates an infrastructure of host and fabric.

        parameters
        ----------
        - host_device: The host device to be used in the infrastructure
        - host_devices: The number of host devices to be represented in the infrastructure
        - fabric: The fabric the hosts will connect to. If none, no host to fabric connections will be made
        - assignment_scheme: the method used to generate the host to fabric connections. if NONE, no host to fabric connections will be made
        - lowest_fabric_switch: the name of the device that the hosts will connect to
        """
        assert isinstance(host_device, bld.DeviceBuilder)
        assert host_devices >= 1
        if fabric:
            super().__init__(fabric=fabric.fabric, hosts=infra.Hosts(devices=infra.DeviceCount(count=host_devices, device=host_device.device)))
        else:
            super().__init__(hosts=infra.Hosts(devices=infra.DeviceCount(count=host_devices, device=host_device.device)))

        if assignment_scheme != "NONE":
            device_link = infra.Link(
                name="eth",
                type=infra.LinkType.LINK_ETHERNET,
            )
            self.infrastructure.links[device_link.name].CopyFrom(device_link)
            distribute_connections = (assignment_scheme == "ROUND_ROBIN")
            self._add_connection(
                link_name=device_link.name,
                lower_device=host_device,
                lower_number_of_devices=host_devices,
                lower_number_of_devices_per_upper_device=fabric.lowest_device.port_down_component.count,
                upper_device=fabric.lowest_device,
                upper_number_of_devices=self.infrastructure.custom_fabric.devices[fabric.lowest_device.device.name].count,
                distribute_connections=distribute_connections
            )
        # get the port down components of the fabric and the port up components of the hosts

        # create the link

        #store link in self.infrastructure.connections

    def _add_connection(
        self,
        link_name: str,
        lower_device: bld.DeviceBuilder,
        lower_number_of_devices: int,
        lower_number_of_devices_per_upper_device: int,
        upper_device: bld.DeviceBuilder,
        upper_number_of_devices: int,
        distribute_connections = False,
    ) -> None:
        """Add a connections between hosts and fabric

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
            # divides hosts evenly between all switches, alternating which switch it is applying a host to
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
        self.infrastructure.connections.extend(connections)