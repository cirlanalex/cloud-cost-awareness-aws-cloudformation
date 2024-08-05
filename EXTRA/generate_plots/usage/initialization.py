from usage.logger.logger import Logger
from usage.database import Database
from controllers.resultActionController import ResultActionController
from controllers.resultPropertyController import ResultPropertyController
from controllers.resultEffectController import ResultEffectController
from controllers.effectController import EffectController
from controllers.actionController import ActionController
from controllers.propertyController import PropertyController

class Initialization:
    def __init__(self, logger: Logger):
        self.db = Database(logger)
        self.resultActionController = ResultActionController(self.db.cursor, self.db.connection)
        self.resultPropertyController = ResultPropertyController(self.db.cursor, self.db.connection)
        self.resultEffectController = ResultEffectController(self.db.cursor, self.db.connection)
        self.effectController = EffectController(self.db.cursor, self.db.connection)
        self.actionController = ActionController(self.db.cursor, self.db.connection)
        self.propertyController = PropertyController(self.db.cursor, self.db.connection)