from usage.logger.logger import Logger
from decouple import config
import mariadb
import sys

class Database:
    def __init__(self, logger: Logger):
        self.connection = self.connect(logger)
        logger.info("Connected to MariaDB Platform")
        self.cursor = self.connection.cursor()
    
    def connect(self, logger: Logger):
        try:
            return mariadb.connect(
                user = config('DATABASE_USER'),
                password = config('DATABASE_PASSWORD'),
                host = '127.0.0.1' if config('DATABASE_HOST') == 'localhost' else config('DATABASE_HOST'),
                port = int(config('DATABASE_PORT')),
                database = config('DATABASE_NAME')
            )
        except mariadb.Error as e:
            logger.error(f"Error connecting to MariaDB Platform: {e}")
            logger.info(f"Error connecting to MariaDB\nExiting...")
            sys.exit(1)

    def close(self):
        self.connection.close()