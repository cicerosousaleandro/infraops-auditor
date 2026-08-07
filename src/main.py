"""
Ponto de entrada do InfraOps Auditor.
"""

from app.application import Application


def main() -> None:
    app = Application()
    app.run()


if __name__ == "__main__":
    main()