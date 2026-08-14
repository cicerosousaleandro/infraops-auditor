"""
Serviço responsável pela persistência das auditorias no banco SQLite.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

from models.device import Device


class DatabaseService:
    """
    Responsável por armazenar e recuperar as auditorias
    realizadas pelo InfraOps Auditor.
    """

    DATABASE_PATH = Path("data/infraops.db")

    @classmethod
    def initialize(cls) -> None:
        """
        Cria o diretório e as tabelas necessárias.

        Também realiza pequenas migrações necessárias
        quando o banco já existe.
        """

        cls.DATABASE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with sqlite3.connect(cls.DATABASE_PATH) as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    network TEXT NOT NULL,
                    scanned_at TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_id INTEGER NOT NULL,
                    ip_address TEXT NOT NULL,
                    hostname TEXT NOT NULL,
                    mac_address TEXT NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (scan_id)
                        REFERENCES scans(id)
                )
                """
            )

            cls._migrate_devices_table(connection)

            connection.commit()

    @staticmethod
    def _migrate_devices_table(
        connection: sqlite3.Connection,
    ) -> None:
        """
        Adiciona novas colunas à tabela devices sem apagar
        os dados das auditorias existentes.
        """

        columns = connection.execute(
            "PRAGMA table_info(devices)"
        ).fetchall()

        column_names = {
            column[1]
            for column in columns
        }

        if "manufacturer" not in column_names:

            connection.execute(
                """
                ALTER TABLE devices
                ADD COLUMN manufacturer TEXT
                DEFAULT 'Desconhecido'
                """
            )

    @classmethod
    def save_scan(
        cls,
        network: str,
        devices: list[Device],
    ) -> int:
        """
        Salva uma auditoria completa e seus dispositivos.

        Retorna o ID da auditoria criada.
        """

        scanned_at = datetime.now().astimezone().isoformat(
            timespec="seconds"
        )

        with sqlite3.connect(cls.DATABASE_PATH) as connection:

            cursor = connection.execute(
                """
                INSERT INTO scans (
                    network,
                    scanned_at
                )
                VALUES (?, ?)
                """,
                (
                    network,
                    scanned_at,
                ),
            )

            scan_id = cursor.lastrowid

            for device in devices:

                connection.execute(
                    """
                    INSERT INTO devices (
                        scan_id,
                        ip_address,
                        hostname,
                        mac_address,
                        status,
                        manufacturer
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        scan_id,
                        device.ip_address,
                        device.hostname,
                        device.mac_address,
                        device.status,
                        device.manufacturer,
                    ),
                )

            connection.commit()

        return scan_id

    @classmethod
    def get_latest_devices(
        cls,
        network: str,
    ) -> list[Device]:
        """
        Recupera os dispositivos encontrados na última
        auditoria realizada para uma determinada rede.
        """

        with sqlite3.connect(cls.DATABASE_PATH) as connection:

            cursor = connection.execute(
                """
                SELECT
                    d.ip_address,
                    d.hostname,
                    d.mac_address,
                    d.status,
                    d.manufacturer
                FROM devices d
                INNER JOIN scans s
                    ON d.scan_id = s.id
                WHERE d.scan_id = (
                    SELECT MAX(id)
                    FROM scans
                    WHERE network = ?
                )
                ORDER BY d.ip_address
                """,
                (network,),
            )

            rows = cursor.fetchall()

        return [
            Device(
                ip_address=row[0],
                hostname=row[1],
                mac_address=row[2],
                status=row[3],
                manufacturer=row[4] or "Desconhecido",
            )
            for row in rows
        ]

    @classmethod
    def get_historical_devices(
        cls,
        network: str,
    ) -> list[Device]:
        """
        Recupera dispositivos encontrados em auditorias
        anteriores da mesma rede.

        A auditoria mais recente dessa rede é excluída
        porque já é recuperada separadamente por
        get_latest_devices().
        """

        with sqlite3.connect(cls.DATABASE_PATH) as connection:

            cursor = connection.execute(
                """
                SELECT
                    d.ip_address,
                    d.hostname,
                    d.mac_address,
                    d.status,
                    d.manufacturer
                FROM devices d
                INNER JOIN scans s
                    ON d.scan_id = s.id
                WHERE s.network = ?
                  AND d.scan_id < (
                      SELECT COALESCE(MAX(id), 0)
                      FROM scans
                      WHERE network = ?
                  )
                ORDER BY d.scan_id DESC, d.ip_address
                """,
                (
                    network,
                    network,
                ),
            )

            rows = cursor.fetchall()

        return [
            Device(
                ip_address=row[0],
                hostname=row[1],
                mac_address=row[2],
                status=row[3],
                manufacturer=row[4] or "Desconhecido",
            )
            for row in rows
        ]