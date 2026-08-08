"""
Serviço responsável pelos cálculos relacionados à rede.
"""

from ipaddress import IPv4Network

from models.network_info import NetworkInfo
from models.network_interface import NetworkInterface


class NetworkService:
    """
    Responsável por calcular informações da rede.
    """

    @staticmethod
    def get_network_info(
        interface: NetworkInterface,
    ) -> NetworkInfo:

        network = IPv4Network(
            f"{interface.ip_address}/{interface.netmask}",
            strict=False,
        )

        hosts = list(network.hosts())

        return NetworkInfo(
            network_address=str(network.network_address),
            broadcast_address=str(network.broadcast_address),
            netmask=str(network.netmask),
            prefix_length=network.prefixlen,
            first_host=str(hosts[0]),
            last_host=str(hosts[-1]),
            total_hosts=len(hosts),
        )