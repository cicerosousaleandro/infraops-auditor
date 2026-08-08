"""
Inicialização da aplicação.
"""

from app.menu import Menu
from services.interface_service import InterfaceService


class Application:
    """
    Classe responsável por controlar o fluxo principal da aplicação.
    """

    def run(self) -> None:
        """
        Inicia a aplicação.
        """

        interfaces = InterfaceService.get_interfaces()

        # ===== DEPURAÇÃO =====
        print("\n=== DEPURAÇÃO ===")
        print(f"Quantidade de interfaces encontradas: {len(interfaces)}")
        print(interfaces)
        print("=================\n")

        Menu.show_interfaces(interfaces)

        while True:

            Menu.show()

            option = input("\nEscolha uma opção: ")

            if option == "0":
                print("\nEncerrando aplicação...")
                break

            print(f"\nA opção '{option}' ainda não foi implementada.\n")

            input("Pressione ENTER para continuar...")