"""
Inicialização da aplicação.
"""

from app.menu import Menu
from services.interface_service import InterfaceService
from services.network_service import NetworkService
from services.scanner_service import ScannerService


class Application:
    """
    Classe responsável por controlar o fluxo principal da aplicação.
    """

    def run(self) -> None:
        """
        Inicia a aplicação.
        """

        interfaces = InterfaceService.get_interfaces()

        Menu.show_interfaces(interfaces)

        selected_interface = Menu.select_interface(interfaces)

        print("\nInterface selecionada")
        print("-" * 50)
        print(f"Nome     : {selected_interface.name}")
        print(f"IPv4     : {selected_interface.ip_address}")
        print(f"Máscara  : {selected_interface.netmask}")
        print("-" * 50)

        network = NetworkService.get_network_info(selected_interface)

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

        print("\nIniciando descoberta de dispositivos...")
        print("Aguarde...\n")

        devices = ScannerService.discover(
            f"{network.network_address}/{network.prefix_length}"
        )

        print(f"Dispositivos encontrados: {len(devices)}\n")

        for device in devices:

            print("-" * 50)
            print(f"IP       : {device.ip_address}")
            print(f"Hostname : {device.hostname}")
            print(f"Status   : {device.status}")

        print("-" * 50)

        input("\nPressione ENTER para continuar...")

        while True:

            Menu.show()

            option = input("\nEscolha uma opção: ")

            if option == "0":
                print("\nEncerrando aplicação...")
                break

            print(f"\nA opção '{option}' ainda não foi implementada.\n")

            input("Pressione ENTER para continuar...")