from models.repo import Repo
from mariadb import Error as mariadbError, Cursor, Connection

class RepoController:
    def __init__(self, dbCursor: Cursor, dbConnection: Connection):
        self.cursor = dbCursor
        self.connection = dbConnection

    def createRepo(self, repo: Repo):
        try:
            self.cursor.execute(f"INSERT INTO repos (url, flag, stop_stage, truncated_1k, truncated_10k) VALUES ('{repo.url}', '{repo.flag}', '{repo.stopStage}', '{repo.truncated1k}', '{repo.truncated10k}')")
            self.connection.commit()
            repo.id = self.cursor.lastrowid
        except mariadbError as e:
            raise mariadbError(f"Failed to create repository {repo.url}: {e}")
    
    def getRepo(self, url: str) -> Repo:
        try:
            self.cursor.execute(f"SELECT * FROM repos WHERE url = '{url}'")
            if self.cursor.rowcount == 0:
                return None
            else:
                for (id, url, flag, stopStage, truncated1k, truncated10k) in self.cursor:
                    return Repo(id, url, flag, stopStage, truncated1k, truncated10k)
        except mariadbError as e:
            raise mariadbError(f"Failed to get repository {url}: {e}")