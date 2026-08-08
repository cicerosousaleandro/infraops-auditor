"""
Interface de terminal do InfraOps Auditor.
"""

from models.network_interface import NetworkInterface


class Menu:

    @staticmethod
    def show() -> None:

        print("\n" + "=" * 50)
        print("          InfraOps Auditor v0.1")
        print("=" * 50)

        print("[1] Scanner de Rede")
        print("[2] Inventário")
        print("[3] Relatórios")
        print("[4] Configurações")
        print("[0] Sair")

        print("=" * 50)

    @staticmethod
    def show_interfaces(
        interfaces: list[NetworkInterface],
    ) -> None:

        print("\nInterfaces disponíveis\n")

        for index, interface in enumerate(interfaces, start=1):

            print("-" * 50)

            print(f"[{index}] {interface.name}")

            print(f"IPv4     : {interface.ip_address}")

            print(f"Máscara  : {interface.netmask}")

        print("-" * 50)

    @staticmethod
    def select_interface(interfaces: list[NetworkInterface]) -> NetworkInterface:
        """
        Permite ao usuário escolher uma interface de rede.
        """

        while True:

            option = input("\nSelecione a interface desejada: ")

            if not option.isdigit():
                print("\nDigite apenas números.")
                continue

            index = int(option)

            if index < 1 or index > len(interfaces):
                print("\nOpção inválida.")
                continue

            return interfaces[index - 1]