from models.plotElement import PlotElement

from mariadb import Error as mariadbError, Cursor, Connection

class EffectController:
    def __init__(self, dbCursor: Cursor, dbConnection: Connection):
        self.cursor = dbCursor
        self.connection = dbConnection

    def getAllEffects(self, table) -> list:
        try:
            query = f"""
            SELECT c.id, c.url, e.effect_id FROM cloudformation.repos r
            INNER JOIN cloudformation.commits c ON c.repo_id = r.id
            INNER JOIN cloudformation.effects_{table} e ON e.commit_id = c.id ORDER BY c.id, e.effect_id
            """
            self.cursor.execute(query)
            if self.cursor.rowcount == 0:
                return None
            else:
                plotElements = []
                for (commitId, commitUrl, effectId) in self.cursor:
                    if len(plotElements) > 0 and plotElements[-1].commitId == commitId:
                        if effectId == 1:
                            plotElements[-1].awareness = True
                        elif effectId == 2:
                            plotElements[-1].increase = True
                        elif effectId == 3:
                            plotElements[-1].save = True
                        elif effectId == 4:
                            plotElements[-1].unrelated = True
                    else:
                        plotElement = PlotElement(commitId, commitUrl.replace("https://api.github.com/repos/", "https://github.com/").replace("/commits/", "/commit/"))
                        if effectId == 1:
                            plotElement.awareness = True
                        elif effectId == 2:
                            plotElement.increase = True
                        elif effectId == 3:
                            plotElement.save = True
                        elif effectId == 4:
                            plotElement.unrelated = True
                        plotElements.append(plotElement)
                return plotElements
        except mariadbError as e:
            raise mariadbError(f"Failed to get all effects: {e}")
    