"""
Inicialização da aplicação.
"""

from app.menu import Menu
from services.interface_service import InterfaceService


class Application:

    def run(self) -> None:

        interfaces = InterfaceService.get_interfaces()

        print("\nInterfaces encontradas:\n")

        for interface in interfaces:
            print(f"Nome     : {interface.name}")
            print(f"IPv4     : {interface.ip_address}")
            print(f"Máscara  : {interface.netmask}")
            print(f"Status   : {'Ativa' if interface.is_up else 'Inativa'}")
            print("-" * 45)

        while True:

            Menu.show()

            option = input("\nEscolha uma opção: ")

            if option == "0":
                print("\nEncerrando aplicação...")
                break

            print(f"\nA opção '{option}' ainda não foi implementada.\n")

            input("Pressione ENTER para continuar...")