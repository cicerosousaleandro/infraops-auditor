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
    changed_devices: list[Device]


class ComparisonService:
    """
    Responsável por identificar alterações entre auditorias.
    """

    @staticmethod
    def compare(
        previous_devices: list[Device],
        current_devices: list[Device],
    ) -> ComparisonResult:
        """
        Compara os dispositivos da auditoria anterior
        com os dispositivos da auditoria atual.
        """

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

        new_devices = []

        for device in current_devices:

            if device.mac_address == "Desconhecido":
                continue

            if device.mac_address not in previous_by_mac:
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
            ):
                changed_devices.append(current_device)

        return ComparisonResult(
            new_devices=new_devices,
            missing_devices=missing_devices,
            changed_devices=changed_devices,
        )