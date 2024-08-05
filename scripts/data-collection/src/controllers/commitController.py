from models.commit import Commit
from mariadb import Error as mariadbError, Cursor, Connection
from controllers.relationKeywordController import RelationKeywordController

class CommitController:
    def __init__(self, dbCursor: Cursor, dbConnection: Connection, relationKeywordInstance: RelationKeywordController):
        self.cursor = dbCursor
        self.connection = dbConnection
        self.relationKeyword = relationKeywordInstance

    def createCommit(self, commit: Commit):
        try:
            self.cursor.execute(f"INSERT INTO commits (repo_id, url, hash, has_non_template) VALUES ('{commit.repoId}', '{commit.url}', '{commit.hash}', '{commit.hasNonTemplate}')")
            lastCommitId = self.cursor.lastrowid
            try:
                self.relationKeyword.createKeywordsToEvent(lastCommitId, commit.keywords, "commit")
                self.connection.commit()
                commit.id = lastCommitId
            except mariadbError as e:
                self.deleteCommit(lastCommitId)
                raise mariadbError(f"Failed to create keywords for commit {commit.url}: {e}")
        except mariadbError as e:
            raise mariadbError(f"Failed to create commit {commit.url}: {e}")
    
    def getCommit(self, commitUrl: str) -> Commit:
        try:
            self.cursor.execute(f"SELECT * FROM commits WHERE url = '{commitUrl}'")
            if self.cursor.rowcount == 0:
                return None
            else:
                for (id, repoId, url, hash, hasNonTemplate) in self.cursor:
                    return Commit(id, repoId, url, hash, [], hasNonTemplate)
        except mariadbError as e:
            raise mariadbError(f"Failed to get commit {commitUrl}: {e}")

    def deleteCommit(self, commitId: int):
        try:
            self.cursor.execute(f"DELETE FROM commits WHERE id = {commitId}")
        except mariadbError as e:
            raise mariadbError(f"Failed to delete commit {commitId}: {e}")