"""RackPlaneHost package

Uses the infra_pb2 protobuf generated code
to capture components, links, and connections of the
RackPlane block diagram.
"""

if __package__ is None or __package__ == "":
    import generated.infra_pb2 as infra
    import builders as bld
else:
    from .generated import infra_pb2 as infra
    from . import builders as bld


class RackPlaneHostBuilder(bld.HostBuilder):
    """
    generates infrastructure of a host that
    supports connecting to switching via multiple planes
    """

    name = "rack plane host"
    description = "a host with dedicated scale up and scale out NICs"

    def __init__(
        self, npu_count: int, scale_up_nic_count: int, scale_out_nic_count: int
    ):
        super(RackPlaneHostBuilder).__init__()
        # 1. Add components
        npu = infra.Component(name="npu", count=npu_count, npu=infra.Npu())
        scale_up_nic = infra.Component(
            name="scale-up-nic", count=scale_up_nic_count, nic=infra.Nic()
        )
        self._port_component = scale_up_nic

        # TODO: Scale OUT NICs
        # scale_out_nic = infra.Component(
        #     name="scale-out-nic", count=scale_out_nic_count, nic=infra.Nic()
        # )

        # 2. Add device
        self._device = infra.Device(
            name=self.name,
            components={
                npu.name: npu,
                scale_up_nic.name: scale_up_nic,
                # scale_out_nic.name: scale_out_nic,
            },
        )

        # 3. Add component links
        # scale UP NICs to NPU connections
        for c1_index in range(npu.count):
            for c2_index in range(scale_up_nic.count):
                self._add_component_link(
                    npu.name,
                    c1_index,
                    f"{npu.name}.{c1_index}.to.{scale_up_nic.name}.{c2_index}",
                    scale_up_nic.name,
                    c2_index,
                )

        # scale OUT NICs to NPU connections
        for c1_index in range(npu.count):
            for c2_index in range(scale_up_nic.count):
                self._add_component_link(
                    npu.name,
                    c1_index,
                    f"{npu.name}.{c1_index=}.to.{scale_up_nic.name}.{c2_index}",
                    scale_up_nic.name,
                    c2_index,
                )

    @property
    def port_up_component(self) -> infra.Component:
        return self._port_component
