"""rack plane related unit tests"""

import pytest

if __package__ is None or __package__ == "":
    from src.generated import infra_pb2
    from src.rack_plane_host import RackPlaneHostBuilder
    from src.rack_plane_fabric import RackPlaneFabricBuilder
    from src.infrastructure import Infrastructure
else:
    from .generated import infra_pb2
    from keysight_chakra.rack_plane_host import RackPlaneHostBuilder
    from keysight_chakra.rack_plane_fabric import RackPlaneFabricBuilder
    from keysight_chakra.infrastructure import Infrastructure


@pytest.mark.parametrize("host_count", [2, 3, 4, 8])
@pytest.mark.parametrize("sup_nic_count", [2, 3, 4])
def test_rack_plane_fabric_and_host(host_count: int, sup_nic_count: int):
    """verifies that the correct infrastructure can be created from rack_plane fabric/host"""
    rp_host_builder = RackPlaneHostBuilder(
        npu_count=1, scale_up_nic_count=sup_nic_count, scale_out_nic_count=1
    )
    rp_fabric_builder = RackPlaneFabricBuilder(host_builder=rp_host_builder)
    infra_builder = Infrastructure(
        host_device=rp_host_builder,
        host_devices=host_count,
        fabric=rp_fabric_builder,
        assignment_scheme="ROUND_ROBIN",
    )
    infrastructure = infra_builder.infrastructure

    assert infrastructure is not None
    # loose check confirming the correct number of connections
    # between host and rack switches
    assert len(infrastructure.connections) == host_count * sup_nic_count


def test_rack_plane_fabric_and_host_detailed():
    """verifies that the correct infrastructure can be created from rack_plane fabric/host"""
    sup_nic_count = 2
    host_count = 2
    rp_host_builder = RackPlaneHostBuilder(
        npu_count=1, scale_up_nic_count=sup_nic_count, scale_out_nic_count=1
    )
    rp_fabric_builder = RackPlaneFabricBuilder(host_builder=rp_host_builder)
    infra_builder = Infrastructure(
        host_device=rp_host_builder,
        host_devices=host_count,
        fabric=rp_fabric_builder,
        assignment_scheme="ROUND_ROBIN",
    )
    infrastructure = infra_builder.infrastructure

    assert infrastructure is not None
    assert len(infrastructure.connections) == host_count * sup_nic_count

    # now let's confirm every details of the DeviceConnections
    def assert_device_conn(
        dev_conn: infra_pb2.DeviceConnection,
        d1_index: int,
        c1_index: int,
        d2_index: int,
        c2_index: int,
    ):
        assert dev_conn.link.d1 == "RackPlaneHost"
        assert dev_conn.link.c1 == "scale-up-nic"
        assert dev_conn.link.d2 == "RackSwitch"
        assert dev_conn.link.c2 == "port-down"
        assert dev_conn.link.link == "eth"
        assert dev_conn.link.d1_index == d1_index
        assert dev_conn.link.c1_index == c1_index
        assert dev_conn.link.d2_index == d2_index
        assert dev_conn.link.c2_index == c2_index

    # plane 0                                        d1,c1,d2,c2
    assert_device_conn(infrastructure.connections[0], 0, 0, 0, 0)
    assert_device_conn(infrastructure.connections[1], 0, 1, 1, 0)
    # plane 1 (and thus rack switch 1; and scale up nic 1 on all hosts)
    assert_device_conn(infrastructure.connections[2], 1, 0, 0, 1)
    assert_device_conn(infrastructure.connections[3], 1, 1, 1, 1)
