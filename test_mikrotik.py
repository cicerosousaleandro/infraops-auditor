from getpass import getpass

from src.services.mikrotik_service import MikroTikService


def main():

    password = getpass("Senha do MikroTik: ")

    try:

        leases = MikroTikService.get_dhcp_leases(
            password
        )

        print()
        print(f"Leases encontrados: {len(leases)}")

        for lease in leases:

            print("-" * 60)
            print(f"IP       : {lease.ip_address}")
            print(f"MAC      : {lease.mac_address}")
            print(f"Hostname : {lease.hostname}")
            print(f"Status   : {lease.status}")

    except Exception as error:

        print()
        print("Falha na consulta DHCP do MikroTik.")
        print(f"Erro: {error}")


if __name__ == "__main__":
    main()