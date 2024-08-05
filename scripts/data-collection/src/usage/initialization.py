from usage.logger.logger import Logger
from usage.database import Database
from controllers.repoController import RepoController
from controllers.relationKeywordController import RelationKeywordController
from controllers.commitController import CommitController

class Initialization:
    def __init__(self, logger: Logger):
        self.db = Database(logger)
        self.repoController = RepoController(self.db.cursor, self.db.connection)
        self.relationKeywordController = RelationKeywordController(self.db.cursor)
        self.commitController = CommitController(self.db.cursor, self.db.connection, self.relationKeywordController)