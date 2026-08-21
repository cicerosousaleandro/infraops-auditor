"""
Configuração da integração com MikroTik.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class MikroTikConfig:
    """
    Armazena as configurações necessárias para conexão
    com um MikroTik.
    """

    host: str
    port: int
    username: str
    password: str