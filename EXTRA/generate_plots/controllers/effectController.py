from models.plotElement import PlotElement

from mariadb import Error as mariadbError, Cursor, Connection

class EffectController:
    def __init__(self, dbCursor: Cursor, dbConnection: Connection):
        self.cursor = dbCursor
        self.connection = dbConnection

    def getAllEffects(self) -> list:
        try:
            query = """
            SELECT c.id, e.effect_id FROM cloudformation.repos r
            INNER JOIN cloudformation.commits c ON c.repo_id = r.id
            INNER JOIN cloudformation.re_effects_commits e ON e.commit_id = c.id WHERE e.effect_id != 4 ORDER BY c.id, e.effect_id
            """
            self.cursor.execute(query)
            if self.cursor.rowcount == 0:
                return None
            else:
                plotElements = []
                for (commitId, effectId) in self.cursor:
                    if len(plotElements) > 0 and plotElements[-1].commitId == commitId:
                        if effectId == 1:
                            plotElements[-1].awareness = True
                        elif effectId == 2:
                            plotElements[-1].increase = True
                        elif effectId == 3:
                            plotElements[-1].save = True
                    else:
                        plotElement = PlotElement(commitId)
                        if effectId == 1:
                            plotElement.awareness = True
                        elif effectId == 2:
                            plotElement.increase = True
                        elif effectId == 3:
                            plotElement.save = True
                        plotElements.append(plotElement)
                return plotElements
        except mariadbError as e:
            raise mariadbError(f"Failed to get all effects: {e}")
    