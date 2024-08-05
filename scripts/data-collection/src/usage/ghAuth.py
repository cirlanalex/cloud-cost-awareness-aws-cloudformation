from usage.logger.logger import Logger
from decouple import config
from github import Github
import sys

class GhAuth(Github):
    def __init__(self, logger: Logger):
        try:
            super().__init__(login_or_token=config('GITHUB_ACCESS_TOKEN'))
            logger.info(f"Connected to Github as {self.get_user().login}")
        except Exception as e:
            logger.error(f"Error connecting to Github: {e}")
            logger.info(f"Error connecting to Github\nExiting...")
            sys.exit(1)