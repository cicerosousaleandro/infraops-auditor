from getpass import getpass

from app.menu import Menu
from config.mikrotik_config import MikroTikConfig
from database.database_service import DatabaseService
from services.comparison_service import ComparisonService
from services.correlation_service import CorrelationService
from services.interface_service import InterfaceService
from services.mikrotik_service import MikroTikService
from services.network_service import NetworkService
from services.scanner_service import ScannerService


class Application:

    def run(self) -> None:

        DatabaseService.initialize()

        # --------------------------------------------------
        # Seleção da interface
        # --------------------------------------------------

        interfaces = InterfaceService.get_interfaces()

        Menu.show_interfaces(interfaces)

        selected_interface = Menu.select_interface(
            interfaces
        )

        print("\nInterface selecionada")
        print("-" * 50)
        print(
            f"Nome     : "
            f"{selected_interface.name}"
        )
        print(
            f"IPv4     : "
            f"{selected_interface.ip_address}"
        )
        print(
            f"Máscara  : "
            f"{selected_interface.netmask}"
        )
        print("-" * 50)

        # --------------------------------------------------
        # Informações da rede
        # --------------------------------------------------

        network = NetworkService.get_network_info(
            selected_interface
        )

        print("\nInformações da Rede")
        print("-" * 50)

        print(
            f"Rede..............: "
            f"{network.network_address}/"
            f"{network.prefix_length}"
        )

        print(
            f"Broadcast.........: "
            f"{network.broadcast_address}"
        )

        print(
            f"Primeiro Host.....: "
            f"{network.first_host}"
        )

        print(
            f"Último Host.......: "
            f"{network.last_host}"
        )

        print(
            f"Hosts Utilizáveis.: "
            f"{network.total_hosts}"
        )

        print("-" * 50)

        network_cidr = (
            f"{network.network_address}/"
            f"{network.prefix_length}"
        )

        # --------------------------------------------------
        # Histórico
        # --------------------------------------------------

        previous_devices = (
            DatabaseService.get_latest_devices(
                network_cidr
            )
        )

        historical_devices = (
            DatabaseService.get_historical_devices(
                network_cidr
            )
        )

        # --------------------------------------------------
        # Scanner
        # --------------------------------------------------

        print(
            "\nIniciando descoberta de dispositivos..."
        )

        print("Aguarde...\n")

        devices = ScannerService.discover(
            network_cidr
        )

        print(
            f"Dispositivos encontrados: "
            f"{len(devices)}"
        )

        # --------------------------------------------------
        # Integração opcional com MikroTik
        # --------------------------------------------------

        print("\nIntegração com MikroTik")
        print("-" * 50)

        password = getpass(
            "Senha do MikroTik: "
        )

        try:

            config = MikroTikConfig(
                host="192.168.3.1",
                port=8728,
                username="am3",
                password=password,
            )

            dhcp_leases = (
                MikroTikService.get_dhcp_leases(
                    config
                )
            )

            correlation = (
                CorrelationService.correlate(
                    devices=devices,
                    leases=dhcp_leases,
                )
            )

            # O MikroTik apenas enriquece os
            # dispositivos já descobertos.

            devices = correlation.devices

            print(
                f"Leases DHCP encontrados: "
                f"{len(dhcp_leases)}"
            )

        except Exception as error:

            print(
                "\nIntegração com MikroTik "
                "não disponível."
            )

            print(
                f"Motivo: {error}"
            )

            print(
                "A auditoria continuará "
                "somente com a descoberta de rede."
            )

        # --------------------------------------------------
        # Resultado consolidado
        # --------------------------------------------------

        print("\nDispositivos identificados")
        print("-" * 50)

        for device in devices:

            print(
                f"IP           : "
                f"{device.ip_address}"
            )

            print(
                f"Hostname     : "
                f"{device.hostname}"
            )

            print(
                f"MAC          : "
                f"{device.mac_address}"
            )

            print(
                f"Fabricante   : "
                f"{device.manufacturer}"
            )

            print(
                f"Status       : "
                f"{device.status}"
            )

            if (
                device.dhcp_status
                != "Não encontrado"
            ):

                print(
                    f"DHCP         : "
                    f"{device.dhcp_status}"
                )

            if (
                device.comment
                != "Sem comentário"
            ):

                print(
                    f"Comentário   : "
                    f"{device.comment}"
                )

            print("-" * 50)

        # --------------------------------------------------
        # Comparação histórica
        # --------------------------------------------------

        if previous_devices:

            comparison = (
                ComparisonService.compare(
                    previous_devices=previous_devices,
                    current_devices=devices,
                    historical_devices=historical_devices,
                )
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

            # --------------------------------------------------
            # Novos dispositivos
            # --------------------------------------------------

            if comparison.new_devices:

                print(
                    "\nNovos dispositivos:"
                )

                for device in (
                    comparison.new_devices
                ):

                    print("-" * 50)

                    print(
                        f"IP         : "
                        f"{device.ip_address}"
                    )

                    print(
                        f"MAC        : "
                        f"{device.mac_address}"
                    )

                    print(
                        f"Hostname   : "
                        f"{device.hostname}"
                    )

                    print(
                        f"Fabricante : "
                        f"{device.manufacturer}"
                    )

                    if (
                        device.dhcp_status
                        != "Não encontrado"
                    ):

                        print(
                            f"DHCP       : "
                            f"{device.dhcp_status}"
                        )

                    if (
                        device.comment
                        != "Sem comentário"
                    ):

                        print(
                            f"Comentário : "
                            f"{device.comment}"
                        )

            # --------------------------------------------------
            # Dispositivos ausentes
            # --------------------------------------------------

            if comparison.missing_devices:

                print(
                    "\nDispositivos ausentes:"
                )

                for device in (
                    comparison.missing_devices
                ):

                    print("-" * 50)

                    print(
                        f"IP anterior : "
                        f"{device.ip_address}"
                    )

                    print(
                        f"MAC         : "
                        f"{device.mac_address}"
                    )

                    print(
                        f"Hostname    : "
                        f"{device.hostname}"
                    )

                    print(
                        f"Fabricante  : "
                        f"{device.manufacturer}"
                    )

                    print(
                        f"Status      : "
                        f"{device.status}"
                    )

            # --------------------------------------------------
            # Dispositivos retornados
            # --------------------------------------------------

            if comparison.returned_devices:

                print(
                    "\nDispositivos retornados:"
                )

                for device in (
                    comparison.returned_devices
                ):

                    print("-" * 50)

                    print(
                        f"IP atual    : "
                        f"{device.ip_address}"
                    )

                    print(
                        f"MAC         : "
                        f"{device.mac_address}"
                    )

                    print(
                        f"Hostname    : "
                        f"{device.hostname}"
                    )

                    print(
                        f"Fabricante  : "
                        f"{device.manufacturer}"
                    )

                    print(
                        f"Status      : "
                        f"{device.status}"
                    )

            # --------------------------------------------------
            # Dispositivos alterados
            # --------------------------------------------------

            if comparison.changed_devices:

                print(
                    "\nDispositivos alterados:"
                )

                for change in (
                    comparison.changed_devices
                ):

                    device = change.device
                    changes = change.changes

                    print("-" * 50)

                    print(
                        f"MAC         : "
                        f"{device.mac_address}"
                    )

                    if len(changes) == 1:

                        print(
                            "Alteração   : ",
                            end="",
                        )

                    else:

                        print(
                            "Alterações  : ",
                            end="",
                        )

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
                            for attribute
                            in changes
                        )
                    )

                    print()

                    for (
                        attribute,
                        values,
                    ) in changes.items():

                        (
                            previous_value,
                            current_value,
                        ) = values

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
                "\nNenhuma auditoria anterior "
                "encontrada."
            )

            print(
                "Esta será a primeira referência "
                "para comparação."
            )

        # --------------------------------------------------
        # Persistência
        # --------------------------------------------------

        scan_id = DatabaseService.save_scan(
            network=network_cidr,
            devices=devices,
        )

        print(
            "\nAuditoria salva com sucesso."
        )

        print(
            f"ID da auditoria: {scan_id}"
        )

        input(
            "\nPressione ENTER para continuar..."
        )

        # --------------------------------------------------
        # Menu
        # --------------------------------------------------

        while True:

            Menu.show()

            option = input(
                "\nEscolha uma opção: "
            )

            if option == "0":

                print(
                    "\nEncerrando aplicação..."
                )

                break

            print(
                f"\nA opção '{option}' "
                "ainda não foi implementada.\n"
            )

            input(
                "Pressione ENTER para continuar..."
            )