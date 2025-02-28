import pytest

from keysight_chakra.infra.service_pb2 import ValidationRequest
from keysight_chakra.infra.infra_pb2 import (
    Infrastructure,
    Inventory,
    Device,
    Link,
    Bandwidth,
    Component,
    DeviceInstances,
)


def test_validate_device(validation, host):
    """Test that a device is valid"""
    response = validation.validate(
        request=ValidationRequest(
            infrastructure=Infrastructure(
                inventory=Inventory(
                    devices={
                        host.name: host,
                    },
                ),
            )
        )
    )
    assert len(response.errors) == 0


def test_missing_bandwidth(validation):
    """Test that a device is missing the bandwidth from a link"""
    device = Device(name="host")
    mii = Link(name="mii")
    device.links[mii.name].CopyFrom(mii)
    inventory = Inventory()
    inventory.devices[device.name].CopyFrom(device)
    infrastructure = Infrastructure(inventory=inventory)
    request = ValidationRequest(infrastructure=infrastructure)
    response = validation.validate(request=request)
    print(response)
    assert len(response.errors) == 1
    assert response.errors[0].WhichOneof("type") == "oneof"


def test_referential_integrity(validation):
    """Referential integrity tests"""
    device = Device(name="laptop")
    mii = Link(name="mii", bandwidth=Bandwidth(gbps=100))
    device.links[mii.name].CopyFrom(mii)
    asic = Component(name="asic", count=1)
    nic = Component(name="nic", count=1)
    device.components[asic.name].CopyFrom(asic)
    device.components[nic.name].CopyFrom(nic)
    device.connections.append(f"bad.device.component.connection")
    device.connections.append(f"{asic.name}.x.{mii.name}.null.-1")
    inventory = Inventory()
    inventory.devices[device.name].CopyFrom(device)
    infrastructure = Infrastructure(inventory=inventory)
    host = DeviceInstances(name="host", device="laptop", count=4)
    infrastructure.device_instances[host.name].CopyFrom(host)
    request = ValidationRequest(infrastructure=infrastructure)
    response = validation.validate(request=request)
    print(response)
    for error in response.errors:
        assert error.WhichOneof("type") == "referential_integrity"


if __name__ == "__main__":
    pytest.main(["-s", "-o", "log_cli=True", "-o", "log_cli_level=INFO", __file__])
