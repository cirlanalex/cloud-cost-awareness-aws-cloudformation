from usage.logger.logger import Logger
from usage.database import Database
from controllers.effectController import EffectController
from controllers.actionController import ActionController
from controllers.propertyController import PropertyController

class Initialization:
    def __init__(self, logger: Logger):
        self.db = Database(logger)
        self.effectController = EffectController(self.db.cursor, self.db.connection)
        self.actionController = ActionController(self.db.cursor, self.db.connection)
        self.propertyController = PropertyController(self.db.cursor, self.db.connection)