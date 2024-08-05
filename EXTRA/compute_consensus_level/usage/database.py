from decouple import config
import mariadb
import sys

class Database:
    def __init__(self):
        self.connection = self.connect()
        print("Connected to MariaDB Platform")
        self.cursor = self.connection.cursor()
    
    def connect(self):
        try:
            return mariadb.connect(
                user = config('DATABASE_USER'),
                password = config('DATABASE_PASSWORD'),
                host = '127.0.0.1' if config('DATABASE_HOST') == 'localhost' else config('DATABASE_HOST'),
                port = int(config('DATABASE_PORT')),
                database = config('DATABASE_NAME')
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            print(f"Error connecting to MariaDB\nExiting...")
            sys.exit(1)

    def close(self):
        self.connection.close()