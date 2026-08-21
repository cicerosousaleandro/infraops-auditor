"""
Serviço responsável pela comunicação com o MikroTik.
"""

import librouteros

from config.mikrotik_config import MikroTikConfig
from models.dhcp_lease import DHCPLease


class MikroTikService:

    @staticmethod
    def connect(config: MikroTikConfig):

        return librouteros.connect(
            host=config.host,
            port=config.port,
            username=config.username,
            password=config.password,
        )

    @classmethod
    def get_identity(
        cls,
        config: MikroTikConfig,
    ) -> str:

        api = cls.connect(config)

        try:

            identity = tuple(
                api.path(
                    "system",
                    "identity",
                )
            )

            return identity[0]["name"]

        finally:

            api.close()

    @classmethod
    def get_dhcp_leases(
        cls,
        config: MikroTikConfig,
    ) -> list[DHCPLease]:

        api = cls.connect(config)

        try:

            leases = tuple(
                api.path(
                    "ip",
                    "dhcp-server",
                    "lease",
                )
            )

            return [
                DHCPLease(
                    ip_address=lease.get(
                        "address",
                        "Desconhecido",
                    ),
                    mac_address=lease.get(
                        "mac-address",
                        "Desconhecido",
                    ),
                    hostname=lease.get(
                        "host-name",
                        "Desconhecido",
                    ),
                    status=lease.get(
                        "status",
                        "Desconhecido",
                    ),
                    comment=lease.get(
                        "comment",
                        "Sem comentário",
                    ),
                )
                for lease in leases
            ]

        finally:

            api.close()