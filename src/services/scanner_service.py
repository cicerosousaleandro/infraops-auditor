"""
Serviço responsável pela descoberta de dispositivos na rede.
"""

import socket

import nmap

from models.device import Device


class ScannerService:
    """
    Responsável por executar a varredura da rede.
    """

    @staticmethod
    def _resolve_hostname(
        ip_address: str,
        nmap_hostname: str,
    ) -> str:
        """
        Tenta resolver o hostname de um dispositivo.

        Primeiro utiliza o hostname descoberto pelo Nmap.
        Caso o Nmap não encontre um nome, tenta resolver
        o endereço IP através do sistema operacional.
        """

        if nmap_hostname:
            return nmap_hostname

        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            return hostname

        except (socket.herror, socket.gaierror, OSError):
            return "Desconhecido"

    @staticmethod
    def _get_manufacturer(
        host_data,
        mac_address: str,
    ) -> str:
        """
        Obtém o fabricante do dispositivo através do OUI/MAC
        identificado pelo Nmap.
        """

        if mac_address == "Desconhecido":
            return "Desconhecido"

        vendor_data = host_data.get("vendor", {})

        if not vendor_data:
            return "Desconhecido"

        manufacturer = vendor_data.get(mac_address)

        if manufacturer:
            return manufacturer

        return "Desconhecido"

    @staticmethod
    def discover(network: str) -> list[Device]:
        """
        Executa a descoberta de dispositivos na rede.
        """

        scanner = nmap.PortScanner()

        scanner.scan(
            hosts=network,
            arguments="-sn",
        )

        devices = []

        for host in scanner.all_hosts():

            host_data = scanner[host]

            nmap_hostname = host_data.hostname()

            hostname = ScannerService._resolve_hostname(
                host,
                nmap_hostname,
            )

            mac_address = host_data["addresses"].get(
                "mac",
                "Desconhecido",
            )

            manufacturer = ScannerService._get_manufacturer(
                host_data,
                mac_address,
            )

            devices.append(
                Device(
                    ip_address=host,
                    hostname=hostname,
                    status=host_data.state(),
                    mac_address=mac_address,
                    manufacturer=manufacturer,
                )
            )

        return devices