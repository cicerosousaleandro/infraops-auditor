import ipaddress
import socket
"""
Descoberta de informações da rede local.


"""

from dataclasses import dataclass
import socket


@dataclass
class NetworkInfo:
    """
    Representa as informações básicas da rede local.
    """

    hostname: str
    ip_address: str


class NetworkService:
    """
    Serviço responsável por obter informações da máquina local.
    """

    @staticmethod
    def get_network_info() -> NetworkInfo:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        return NetworkInfo(
            hostname=hostname,
            ip_address=ip_address,
        )