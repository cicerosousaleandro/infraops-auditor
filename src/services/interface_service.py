"""
Serviço responsável por descobrir as interfaces de rede disponíveis.
"""

import socket

import psutil

from models.network_interface import NetworkInterface


class InterfaceService:
    """
    Responsável por obter informações das interfaces de rede.
    """

    @staticmethod
    def get_interfaces() -> list[NetworkInterface]:
        interfaces = []

        addresses = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        for interface_name, address_list in addresses.items():

            is_up = (
                stats.get(interface_name).isup
                if interface_name in stats
                else False
            )

            for address in address_list:

                if address.family == socket.AF_INET:

                    interfaces.append(
                        NetworkInterface(
                            name=interface_name,
                            ip_address=address.address,
                            netmask=address.netmask,
                            is_up=is_up,
                        )
                    )

        return interfaces