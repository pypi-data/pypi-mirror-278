import json
import logging
from typing import Dict, Any
from .AppSettings import AppSettings
import mysql.connector


logger = logging.getLogger(__name__)

class MySQLSetting(AppSettings):
    """App Settings stored in a MySQL database."""

    def __init__(
        self,
        session_id: str,
        host: str = "172.18.0.11",
        user: str = "default",
        password: str = "your_password",
        database: str = "your_database",
        table: str = "settings",
    ):
        try:
            import mysql.connector
        except ImportError:
            raise ImportError(
                "Could not import mysql-connector-python python package. "
                "Please install it with `pip install mysql-connector-python`."
            )

        self.db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
        }
        self.session_id = session_id
        self.table = table
        self.create_database_if_not_exists()
        self.create_table_if_not_exists()


    def create_database_if_not_exists(self):
        """Create the database if it doesn't exist"""
        db_config_without_db = {
            "host": self.db_config["host"],
            "user": self.db_config["user"],
            "password": self.db_config["password"],
        }
        with mysql.connector.connect(**db_config_without_db) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    CREATE DATABASE IF NOT EXISTS {self.db_config['database']}
                """)
                connection.commit()

    def create_table_if_not_exists(self):
        """Create the table if it doesn't exist"""
        with mysql.connector.connect(**self.db_config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.table} (
                        session_id VARCHAR(255) PRIMARY KEY,
                        settings JSON
                    )
                """)
                connection.commit()

    def get_settings(self) -> Dict:
        """Retrieve the settings from MySQL"""
        with mysql.connector.connect(**self.db_config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT settings FROM {self.table}
                    WHERE session_id = %s
                """, (self.session_id,))
                result = cursor.fetchone()
                if result:
                    return json.loads(result[0])
        return {}

    def update_settings(self, settings: Dict) -> None:
        """Update the settings in MySQL"""
        with mysql.connector.connect(**self.db_config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    REPLACE INTO {self.table} (session_id, settings)
                    VALUES (%s, %s)
                """, (self.session_id, json.dumps(settings)))
                connection.commit()

    def clear_settings(self) -> None:
        """Clear session settings from MySQL"""
        with mysql.connector.connect(**self.db_config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    DELETE FROM {self.table}
                    WHERE session_id = %s
                """, (self.session_id,))
                connection.commit()

    def set_setting(self, key: str, value: Any) -> None:
        """Set a specific setting in MySQL"""
        with mysql.connector.connect(**self.db_config) as connection:
            with connection.cursor() as cursor:
                # Retrieve the current settings
                cursor.execute(f"""
                    SELECT settings FROM {self.table}
                    WHERE session_id = %s
                """, (self.session_id,))
                result = cursor.fetchone()
                current_settings = json.loads(result[0]) if result else {}

                # Update the specific setting
                current_settings[key] = value

                # Save the updated settings
                cursor.execute(f"""
                    REPLACE INTO {self.table} (session_id, settings)
                    VALUES (%s, %s)
                """, (self.session_id, json.dumps(current_settings)))
                connection.commit()