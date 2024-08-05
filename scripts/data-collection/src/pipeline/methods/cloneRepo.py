from git import Repo as GitRepo
from subprocess import Popen

def cloneRepoThread(self, repoUrl: str):
        try:
            self.logger.info(f"Cloning repository {repoUrl}", 2)
            GitRepo.clone_from(repoUrl, "temp_repo", depth=10001, no_checkout=True)

            # enable sparse checkout to only checkout the needed files
            process = Popen(["git", "-C", "temp_repo", "config", "core.sparseCheckout", "true"])
            process.wait()
        except Exception:
            raise