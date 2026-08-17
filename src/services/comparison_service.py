from dataclasses import dataclass

from models.device import Device


@dataclass(slots=True)
class DeviceChange:
    device: Device
    changes: dict[str, tuple[str, str]]


@dataclass(slots=True)
class ComparisonResult:
    new_devices: list[Device]
    missing_devices: list[Device]
    returned_devices: list[Device]
    changed_devices: list[DeviceChange]


class ComparisonService:

    @staticmethod
    def compare(
        previous_devices: list[Device],
        current_devices: list[Device],
        historical_devices: list[Device] | None = None,
    ) -> ComparisonResult:

        if historical_devices is None:
            historical_devices = []

        previous_by_mac = {
            device.mac_address: device
            for device in previous_devices
            if device.mac_address != "Desconhecido"
        }

        current_by_mac = {
            device.mac_address: device
            for device in current_devices
            if device.mac_address != "Desconhecido"
        }

        historical_macs = {
            device.mac_address
            for device in historical_devices
            if device.mac_address != "Desconhecido"
        }

        new_devices = []
        returned_devices = []

        for device in current_devices:

            if device.mac_address == "Desconhecido":
                continue

            if device.mac_address in previous_by_mac:
                continue

            if device.mac_address in historical_macs:
                returned_devices.append(device)
            else:
                new_devices.append(device)

        missing_devices = []

        for device in previous_devices:

            if device.mac_address == "Desconhecido":
                continue

            if device.mac_address not in current_by_mac:
                missing_devices.append(device)

        changed_devices = []

        for mac_address, current_device in current_by_mac.items():

            previous_device = previous_by_mac.get(mac_address)

            if previous_device is None:
                continue

            changes = {}

            if previous_device.ip_address != current_device.ip_address:
                changes["ip_address"] = (
                    previous_device.ip_address,
                    current_device.ip_address,
                )

            if previous_device.hostname != current_device.hostname:
                changes["hostname"] = (
                    previous_device.hostname,
                    current_device.hostname,
                )

            if previous_device.status != current_device.status:
                changes["status"] = (
                    previous_device.status,
                    current_device.status,
                )

            if previous_device.manufacturer != current_device.manufacturer:
                changes["manufacturer"] = (
                    previous_device.manufacturer,
                    current_device.manufacturer,
                )

            if changes:
                changed_devices.append(
                    DeviceChange(
                        device=current_device,
                        changes=changes,
                    )
                )

        return ComparisonResult(
            new_devices=new_devices,
            missing_devices=missing_devices,
            returned_devices=returned_devices,
            changed_devices=changed_devices,
        )