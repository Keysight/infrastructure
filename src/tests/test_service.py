import pytest
from service import Service
from generated.service_pb2 import ValidationRequest
from generated.infra_pb2 import Infrastructure, Inventory, Device, Link, LinkType, Bandwidth, Component


def test_valid_device(device):
    """Test that a device is valid"""
    mii = Link(name="mii", type=LinkType.LINK_CUSTOM, bandwidth=Bandwidth(gbps=100))
    device.links[mii.name].CopyFrom(mii)
    inventory = Inventory()
    inventory.devices[device.name].CopyFrom(device)
    infrastructure = Infrastructure(inventory=inventory)
    request = ValidationRequest(infrastructure=infrastructure)
    response = Service().validate(request=request)
    assert len(response.errors) == 0


def test_missing_bandwidth():
    """Test that a device is missing the bandwidth from a link"""
    device = Device(name="host")
    mii = Link(name="mii", type=LinkType.LINK_CUSTOM)
    device.links[mii.name].CopyFrom(mii)
    inventory = Inventory()
    inventory.devices[device.name].CopyFrom(device)
    infrastructure = Infrastructure(inventory=inventory)
    request = ValidationRequest(infrastructure=infrastructure)
    response = Service().validate(request=request)
    print(response)
    assert len(response.errors) == 1
    assert response.errors[0].WhichOneof("type") == "oneof"


def test_invalid_component_connection():
    """Test that a component connection is valid"""
    device = Device(name="host")
    mii = Link(name="mii", type=LinkType.LINK_CUSTOM, bandwidth=Bandwidth(gbps=100))
    device.links[mii.name].CopyFrom(mii)
    asic = Component(name="asic", count=1)
    nic = Component(name="nic", count=1)
    device.components[asic.name].CopyFrom(asic)
    device.components[nic.name].CopyFrom(nic)
    device.connections.append(f"{asic.name}.x.{mii.name}.null.-1")
    inventory = Inventory()
    inventory.devices[device.name].CopyFrom(device)
    infrastructure = Infrastructure(inventory=inventory)
    request = ValidationRequest(infrastructure=infrastructure)
    response = Service().validate(request=request)
    print(response)
    assert len(response.errors) == 3
    assert response.errors[0].WhichOneof("type") == "connection"


if __name__ == "__main__":
    pytest.main(["-s", "-o", "log_cli=True", "-o", "log_cli_level=INFO", __file__])
