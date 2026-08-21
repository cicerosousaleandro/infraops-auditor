"""
Model que representa um lease DHCP obtido do MikroTik.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class DHCPLease:
    """
    Representa um lease DHCP fornecido pelo MikroTik.
    """

    ip_address: str
    mac_address: str
    hostname: str
    status: str
    comment: str = "Sem comentário"