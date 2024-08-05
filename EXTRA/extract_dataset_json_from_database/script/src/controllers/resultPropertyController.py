from mariadb import Error as mariadbError, Cursor, Connection

class ResultPropertyController:
    def __init__(self, dbCursor: Cursor, dbConnection: Connection):
        self.cursor = dbCursor
        self.connection = dbConnection

    def getProperties(self, propertyId: int) -> list:
        try:
            query = """
            SELECT r.url, c.url FROM cloudformation.repos r
            INNER JOIN cloudformation.commits c ON c.repo_id = r.id
            INNER JOIN cloudformation.re_effects_commits e ON e.commit_id = c.id
            INNER JOIN cloudformation.re_actions_commits a ON a.commit_id = c.id
            INNER JOIN cloudformation.re_properties_commits p ON p.commit_id = c.id WHERE p.property_id = ?
            """
            self.cursor.execute(query, (propertyId,))
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
            raise mariadbError(f"Failed to get repositories for property {propertyId}: {e}")