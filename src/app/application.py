"""
Inicialização da aplicação.
"""

from app.menu import Menu


class Application:

    def run(self) -> None:

        while True:

            Menu.show()

            option = input("\nEscolha uma opção: ")

            if option == "0":
                print("\nEncerrando aplicação...")
                break

            print(f"\nA opção '{option}' ainda não foi implementada.\n")

            input("Pressione ENTER para continuar...")