"""
Model que representa um dispositivo encontrado na rede.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Device:
    """
    Representa um dispositivo identificado durante a varredura.
    """

    ip_address: str
    hostname: str
    status: str
    mac_address: str