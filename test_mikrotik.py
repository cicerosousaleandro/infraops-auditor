from getpass import getpass

from src.services.mikrotik_service import MikroTikService


def main() -> None:

    password = getpass("Senha do MikroTik: ")

    api = MikroTikService.connect(password)

    try:

        leases = list(
            api.path(
                "ip",
                "dhcp-server",
                "lease",
            )
        )

        print()
        print(f"Leases encontrados: {len(leases)}")

        for index, lease in enumerate(leases, start=1):

            print()
            print("=" * 60)
            print(f"LEASE #{index}")
            print("=" * 60)

            for key, value in sorted(lease.items()):

                print(f"{key:<25}: {value}")

    finally:

        api.close()


if __name__ == "__main__":
    main()