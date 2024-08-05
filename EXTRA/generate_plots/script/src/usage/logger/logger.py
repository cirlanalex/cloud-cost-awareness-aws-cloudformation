import os

class Logger:
    def __init__(self):
        if not os.path.exists("usage/logger/logs"):
            os.makedirs("usage/logger/logs")
        self.log_file = os.path.join("usage/logger/logs", "log.txt")
        self.error_file = os.path.join("usage/logger/logs", "error_log.txt")
        self.db_file = os.path.join("usage/logger/logs", "db_log.txt")

    def error(self, error: str):
        with open(self.error_file, "a") as file:
            file.write(f"ERROR: {error}\n")

    def info(self, info: str, tabs: int = 0):
        for _ in range(tabs):
            info = f"\t{info}"
        print(info)
        with open(self.log_file, "a") as file:
            file.write(f"{info}\n")

    def dbError(self, error: str):
        with open(self.db_file, "a") as file:
            file.write(f"ERROR: {error}\n")
    