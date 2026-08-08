"""
Inicialização da aplicação.
"""

from app.menu import Menu
from services.interface_service import InterfaceService
from services.network_service import NetworkService


class Application:
    """
    Classe responsável por controlar o fluxo principal da aplicação.
    """

    def run(self) -> None:
        """
        Inicia a aplicação.
        """

        # Descobre as interfaces disponíveis
        interfaces = InterfaceService.get_interfaces()

        # ===== DEPURAÇÃO =====
        print("\n=== DEPURAÇÃO ===")
        print(f"Quantidade de interfaces encontradas: {len(interfaces)}")
        print(interfaces)
        print("=================\n")

        # Exibe as interfaces
        Menu.show_interfaces(interfaces)

        # Usuário escolhe uma interface
        selected_interface = Menu.select_interface(interfaces)

        # Calcula as informações da rede
        network_info = NetworkService.get_network_info(
            selected_interface
        )

        # Interface escolhida
        print("\nInterface selecionada")
        print("-" * 50)
        print(f"Nome     : {selected_interface.name}")
        print(f"IPv4     : {selected_interface.ip_address}")
        print(f"Máscara  : {selected_interface.netmask}")
        print("-" * 50)

        # Informações da rede
        print("\nInformações da Rede")
        print("-" * 50)
        print(f"Rede..............: {network_info.network_address}/{network_info.prefix_length}")
        print(f"Broadcast.........: {network_info.broadcast_address}")
        print(f"Primeiro Host.....: {network_info.first_host}")
        print(f"Último Host.......: {network_info.last_host}")
        print(f"Hosts Utilizáveis.: {network_info.total_hosts}")
        print("-" * 50)

        while True:

            Menu.show()

            option = input("\nEscolha uma opção: ")

            if option == "0":
                print("\nEncerrando aplicação...")
                break

            print(f"\nA opção '{option}' ainda não foi implementada.\n")

            input("Pressione ENTER para continuar...")