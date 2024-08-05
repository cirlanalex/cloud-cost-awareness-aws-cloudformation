from datetime import datetime
from time import sleep
from usage.ghAuth import GhAuth
from usage.logger.logger import Logger

def checkGhLimits(github: GhAuth, limit: int, logger: Logger = None):
    core_limit = github.get_rate_limit().core
    if core_limit.remaining < limit:
        sleepTime = core_limit.reset.timestamp() - datetime.now().timestamp()
        if logger:
            logger.info(f"GitHub limit reached, sleeping for {int(sleepTime)} seconds")
        sleep(sleepTime)
