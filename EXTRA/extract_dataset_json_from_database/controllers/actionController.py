from models.plotElement import PlotElement

from mariadb import Error as mariadbError, Cursor, Connection

class ActionController:
    def __init__(self, dbCursor: Cursor, dbConnection: Connection):
        self.cursor = dbCursor
        self.connection = dbConnection

    def getActionsOfCommit(self, plotElement: PlotElement):
        try:
            query = """
            SELECT a.action_id FROM cloudformation.repos r
            INNER JOIN cloudformation.commits c ON c.repo_id = r.id
            INNER JOIN cloudformation.re_effects_commits e ON e.commit_id = c.id
            INNER JOIN cloudformation.re_actions_commits a ON a.commit_id = c.id WHERE c.id = ? ORDER BY a.action_id
            """
            self.cursor.execute(query, (plotElement.commitId,))
            if self.cursor.rowcount == 0:
                return None
            else:
                for (actionId,) in self.cursor:
                    if actionId == 1:
                        plotElement.change = True
                    elif actionId == 2:
                        plotElement.test = True
                    elif actionId == 3:
                        plotElement.track = True
        except mariadbError as e:
            raise mariadbError(f"Failed to get actions for commit {plotElement.commitId}: {e}")