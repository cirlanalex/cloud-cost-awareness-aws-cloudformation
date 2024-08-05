from mariadb import Error as mariadbError
from models.commit import Commit
from models.repo import Repo

def postNewCommit(self, commit: object, repo: Repo):
        try:
            dbRepo = self.instance.repoController.getRepo(repo.url)
            if dbRepo is None:
                self.instance.repoController.createRepo(repo)
            dbCommit = Commit(None, repo.id, commit['commit_url'], commit['commit_hash'], commit['keywords'], commit['has_non_template'])
            self.instance.commitController.createCommit(dbCommit)
        except mariadbError:
            raise