from dataclasses import dataclass


@dataclass(slots=True)
class DHCPLease:
    ip_address: str
    mac_address: str
    hostname: str
    status: str