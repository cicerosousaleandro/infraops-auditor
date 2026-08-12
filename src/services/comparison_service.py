"""
Serviço responsável por comparar auditorias de rede.
"""

from dataclasses import dataclass

from models.device import Device


@dataclass(slots=True)
class ComparisonResult:
    """
    Representa o resultado da comparação entre duas auditorias.
    """

    new_devices: list[Device]
    missing_devices: list[Device]
    returned_devices: list[Device]
    changed_devices: list[Device]


class ComparisonService:
    """
    Responsável por identificar alterações entre auditorias.
    """

    @staticmethod
    def compare(
        previous_devices: list[Device],
        current_devices: list[Device],
        historical_devices: list[Device] | None = None,
    ) -> ComparisonResult:
        """
        Compara a auditoria anterior com a auditoria atual.

        O MAC Address é utilizado como identidade principal
        do dispositivo.
        """

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

            if (
                previous_device.ip_address
                != current_device.ip_address
                or previous_device.hostname
                != current_device.hostname
                or previous_device.status
                != current_device.status
                or previous_device.manufacturer
                != current_device.manufacturer
            ):
                changed_devices.append(current_device)

        return ComparisonResult(
            new_devices=new_devices,
            missing_devices=missing_devices,
            returned_devices=returned_devices,
            changed_devices=changed_devices,
        )