"""
Model que representa uma interface de rede.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class NetworkInterface:
    """
    Representa uma interface de rede encontrada no sistema.
    """

    name: str
    ip_address: str
    netmask: str
    is_up: bool