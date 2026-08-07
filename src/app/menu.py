"""
Módulo responsável pela interface principal do InfraOps Auditor.
"""


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