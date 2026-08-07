"""
Inicialização da aplicação.
"""

from app.menu import Menu
from scanner.network import NetworkService


class Application:

    def run(self) -> None:

        network = NetworkService.get_network_info()

        print("\nInformações da máquina:")
        print(f"Hostname: {network.hostname}")
        print(f"IP: {network.ip_address}")
        print()

        while True:

            Menu.show()

            option = input("\nEscolha uma opção: ")

            if option == "0":
                print("\nEncerrando aplicação...")
                break

            print(f"\nA opção '{option}' ainda não foi implementada.\n")

            input("Pressione ENTER para continuar...")