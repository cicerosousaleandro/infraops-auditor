from app.menu import Menu
from database.database_service import DatabaseService
from services.comparison_service import ComparisonService
from services.interface_service import InterfaceService
from services.network_service import NetworkService
from services.scanner_service import ScannerService


class Application:

    def run(self) -> None:

        DatabaseService.initialize()

        interfaces = InterfaceService.get_interfaces()

        Menu.show_interfaces(interfaces)

        selected_interface = Menu.select_interface(interfaces)

        print("\nInterface selecionada")
        print("-" * 50)
        print(f"Nome     : {selected_interface.name}")
        print(f"IPv4     : {selected_interface.ip_address}")
        print(f"Máscara  : {selected_interface.netmask}")
        print("-" * 50)

        network = NetworkService.get_network_info(
            selected_interface
        )

        print("\nInformações da Rede")
        print("-" * 50)

        print(
            f"Rede..............: "
            f"{network.network_address}/{network.prefix_length}"
        )

        print(f"Broadcast.........: {network.broadcast_address}")
        print(f"Primeiro Host.....: {network.first_host}")
        print(f"Último Host.......: {network.last_host}")
        print(f"Hosts Utilizáveis.: {network.total_hosts}")
        print("-" * 50)

        network_cidr = (
            f"{network.network_address}/{network.prefix_length}"
        )

        previous_devices = DatabaseService.get_latest_devices(
            network_cidr
        )

        historical_devices = (
            DatabaseService.get_historical_devices(
                network_cidr
            )
        )

        print("\nIniciando descoberta de dispositivos...")
        print("Aguarde...\n")

        devices = ScannerService.discover(network_cidr)

        print(
            f"Dispositivos encontrados: {len(devices)}\n"
        )

        for device in devices:

            print("-" * 50)
            print(f"IP           : {device.ip_address}")
            print(f"Hostname     : {device.hostname}")
            print(f"MAC          : {device.mac_address}")
            print(f"Fabricante   : {device.manufacturer}")
            print(f"Status       : {device.status}")

        print("-" * 50)

        if previous_devices:

            comparison = ComparisonService.compare(
                previous_devices=previous_devices,
                current_devices=devices,
                historical_devices=historical_devices,
            )

            print("\nResultado da comparação")
            print("-" * 50)

            print(
                f"Novos dispositivos........: "
                f"{len(comparison.new_devices)}"
            )

            print(
                f"Dispositivos ausentes......: "
                f"{len(comparison.missing_devices)}"
            )

            print(
                f"Dispositivos retornados.....: "
                f"{len(comparison.returned_devices)}"
            )

            print(
                f"Dispositivos alterados......: "
                f"{len(comparison.changed_devices)}"
            )

            if comparison.new_devices:

                print("\nNovos dispositivos:")

                for device in comparison.new_devices:

                    print("-" * 50)
                    print(f"IP         : {device.ip_address}")
                    print(f"MAC        : {device.mac_address}")
                    print(f"Hostname   : {device.hostname}")
                    print(f"Fabricante : {device.manufacturer}")

            if comparison.missing_devices:

                print("\nDispositivos ausentes:")

                for device in comparison.missing_devices:

                    print("-" * 50)
                    print(f"IP anterior : {device.ip_address}")
                    print(f"MAC         : {device.mac_address}")
                    print(f"Hostname    : {device.hostname}")
                    print(f"Fabricante  : {device.manufacturer}")
                    print(f"Status      : {device.status}")

            if comparison.returned_devices:

                print("\nDispositivos retornados:")

                for device in comparison.returned_devices:

                    print("-" * 50)
                    print(f"IP atual    : {device.ip_address}")
                    print(f"MAC         : {device.mac_address}")
                    print(f"Hostname    : {device.hostname}")
                    print(f"Fabricante  : {device.manufacturer}")
                    print(f"Status      : {device.status}")

            if comparison.changed_devices:

                print("\nDispositivos alterados:")

                for change in comparison.changed_devices:

                    device = change.device
                    changes = change.changes

                    print("-" * 50)
                    print(f"MAC         : {device.mac_address}")

                    if len(changes) == 1:
                        print("Alteração   : ", end="")

                    else:
                        print("Alterações  : ", end="")

                    labels = {
                        "ip_address": "endereço IP",
                        "hostname": "hostname",
                        "status": "status",
                        "manufacturer": "fabricante",
                    }

                    print(
                        ", ".join(
                            labels.get(
                                attribute,
                                attribute,
                            )
                            for attribute in changes
                        )
                    )

                    print()

                    for attribute, values in changes.items():

                        previous_value, current_value = values

                        labels = {
                            "ip_address": "IP",
                            "hostname": "Hostname",
                            "status": "Status",
                            "manufacturer": "Fabricante",
                        }

                        label = labels.get(
                            attribute,
                            attribute,
                        )

                        print(
                            f"{label} anterior : "
                            f"{previous_value}"
                        )

                        print(
                            f"{label} atual    : "
                            f"{current_value}"
                        )

                        print()

            print("-" * 50)

        else:

            print(
                "\nNenhuma auditoria anterior encontrada."
            )

            print(
                "Esta será a primeira referência "
                "para comparação."
            )

        scan_id = DatabaseService.save_scan(
            network=network_cidr,
            devices=devices,
        )

        print(
            f"\nAuditoria salva com sucesso."
            f"\nID da auditoria: {scan_id}"
        )

        input("\nPressione ENTER para continuar...")

        while True:

            Menu.show()

            option = input("\nEscolha uma opção: ")

            if option == "0":

                print("\nEncerrando aplicação...")
                break

            print(
                f"\nA opção '{option}' "
                "ainda não foi implementada.\n"
            )

            input("Pressione ENTER para continuar...")