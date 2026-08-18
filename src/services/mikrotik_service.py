import librouteros

from src.models.dhcp_lease import DHCPLease


class MikroTikService:

    HOST = "192.168.3.1"
    PORT = 8728
    USERNAME = "am3"

    @classmethod
    def connect(cls, password: str):

        return librouteros.connect(
            host=cls.HOST,
            port=cls.PORT,
            username=cls.USERNAME,
            password=password,
        )

    @classmethod
    def get_identity(cls, password: str) -> str:

        api = cls.connect(password)

        try:

            identity = tuple(
                api.path("system", "identity")
            )

            return identity[0]["name"]

        finally:

            api.close()

    @classmethod
    def get_dhcp_leases(
        cls,
        password: str,
    ) -> list[DHCPLease]:

        api = cls.connect(password)

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
                )
                for lease in leases
            ]

        finally:

            api.close()