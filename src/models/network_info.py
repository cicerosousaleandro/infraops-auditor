"""
Model que representa informações de uma rede IPv4.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class NetworkInfo:
    """
    Representa as informações calculadas de uma rede IPv4.
    """

    network_address: str
    broadcast_address: str
    netmask: str
    prefix_length: int
    first_host: str
    last_host: str
    total_hosts: int