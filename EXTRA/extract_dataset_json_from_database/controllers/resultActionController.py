from mariadb import Error as mariadbError, Cursor, Connection

class ResultActionController:
    def __init__(self, dbCursor: Cursor, dbConnection: Connection):
        self.cursor = dbCursor
        self.connection = dbConnection

    def getActions(self, actionId: int) -> list:
        try:
            query = """
            SELECT r.url, c.url FROM cloudformation.repos r
            INNER JOIN cloudformation.commits c ON c.repo_id = r.id
            INNER JOIN cloudformation.re_effects_commits e ON e.commit_id = c.id
            INNER JOIN cloudformation.re_actions_commits a ON a.commit_id = c.id WHERE a.action_id = ?
            """
            self.cursor.execute(query, (actionId,))
            if self.cursor.rowcount == 0:
                return None, None
            else:
                repos = []
                commits = []
                for (url, curl) in self.cursor:
                    repos.append(url)
                    commits.append(curl)
                return repos, commits
        except mariadbError as e:
            raise mariadbError(f"Failed to get repositories for action {actionId}: {e}")