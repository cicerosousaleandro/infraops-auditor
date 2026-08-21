"""
Serviço responsável por correlacionar dispositivos descobertos
com informações provenientes do MikroTik.
"""

from dataclasses import dataclass

from models.device import Device
from models.dhcp_lease import DHCPLease


@dataclass(slots=True)
class CorrelationResult:
    """
    Resultado da correlação entre descoberta de rede e DHCP.
    """

    devices: list[Device]
    unmatched_leases: list[DHCPLease]


class CorrelationService:

    @staticmethod
    def correlate(
        devices: list[Device],
        leases: list[DHCPLease],
    ) -> CorrelationResult:

        leases_by_ip = {
            lease.ip_address: lease
            for lease in leases
            if lease.ip_address != "Desconhecido"
        }

        leases_by_mac = {
            lease.mac_address.lower(): lease
            for lease in leases
            if lease.mac_address != "Desconhecido"
        }

        correlated_devices = []

        matched_lease_ips = set()

        for device in devices:

            lease = None

            if device.ip_address in leases_by_ip:

                lease = leases_by_ip[
                    device.ip_address
                ]

            elif (
                device.mac_address != "Desconhecido"
                and device.mac_address.lower()
                in leases_by_mac
            ):

                lease = leases_by_mac[
                    device.mac_address.lower()
                ]

            if lease is None:

                correlated_devices.append(
                    device
                )

                continue

            matched_lease_ips.add(
                lease.ip_address
            )

            hostname = device.hostname

            if hostname == "Desconhecido":
                hostname = lease.hostname

            mac_address = device.mac_address

            if mac_address == "Desconhecido":
                mac_address = lease.mac_address

            dhcp_status = lease.status

            comment = lease.comment

            enriched_device = Device(
                ip_address=device.ip_address,
                hostname=hostname,
                status=device.status,
                mac_address=mac_address,
                manufacturer=device.manufacturer,
                dhcp_status=dhcp_status,
                comment=comment,
            )

            correlated_devices.append(
                enriched_device
            )

        unmatched_leases = [
            lease
            for lease in leases
            if lease.ip_address
            not in matched_lease_ips
        ]

        return CorrelationResult(
            devices=correlated_devices,
            unmatched_leases=unmatched_leases,
        )