"""
Serviço responsável pela descoberta de dispositivos na rede.
"""

import nmap

from models.device import Device


class ScannerService:
    """
    Responsável por executar a varredura da rede.
    """

    @staticmethod
    def discover(network: str) -> list[Device]:

        scanner = nmap.PortScanner()

        scanner.scan(
            hosts=network,
            arguments="-sn"
        )

        devices = []

        for host in scanner.all_hosts():

            hostname = scanner[host].hostname()

            if not hostname:
                hostname = "Desconhecido"

            mac_address = scanner[host]["addresses"].get(
                "mac",
                "Desconhecido"
            )

            devices.append(
                Device(
                    ip_address=host,
                    hostname=hostname,
                    status=scanner[host].state(),
                    mac_address=mac_address,
                )
            )

        return devices