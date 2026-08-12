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
    def _resolve_hostname(ip_address: str, nmap_hostname: str) -> str:
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
    def discover(network: str) -> list[Device]:
        """
        Executa a descoberta de dispositivos na rede.
        """

        scanner = nmap.PortScanner()

        scanner.scan(
            hosts=network,
            arguments="-sn"
        )

        devices = []

        for host in scanner.all_hosts():

            nmap_hostname = scanner[host].hostname()

            hostname = ScannerService._resolve_hostname(
                host,
                nmap_hostname
            )

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