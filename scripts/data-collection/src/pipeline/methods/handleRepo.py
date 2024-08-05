import os
from git import Repo as GitRepo
from github import GithubException
from threading import Thread
from subprocess import Popen
from mariadb import Error as mariadbError
from models.repo import Repo

def handleRepoForCommit(self, ghRepoUrl: object):
        repoUrl = ghRepoUrl.replace("https://api.github.com/repos/", "https://github.com/")
        self.logger.info(f"Processing repository {repoUrl}", 1)
        try:
            repo = self.instance.repoController.getRepo(repoUrl)
            try:
                if repo is not None:
                    self.logger.info(f"Repository {repoUrl} already checked", 2)
                    return
                
                # use the GitHub API to check the repository size
                ghRepo = self.github.get_repo(repoUrl.replace("https://github.com/", ""))
                if ghRepo.size > 5000000:
                    self.logger.info(f"Repository {repoUrl} is too large: {ghRepo.size / 1000000}GB", 2)
                    repo = Repo(None, repoUrl, 'skipped', 'keywords', 'No', 'No')
                    self.instance.repoController.createRepo(repo)
                    return
                repo = Repo(None, repoUrl, None, 'keywords', 'No', 'No')

                # set the repository as truncated if it has more than 1000 or 10000 commits
                commitsCount = ghRepo.get_commits().totalCount
                if commitsCount > 1000:
                    repo.truncated1k = 'Yes'
                else:
                    repo.truncated1k = 'No'
                if commitsCount > 10000:
                    repo.truncated10k = 'Yes'
                else:
                    repo.truncated10k = 'No'

                # clone the repository with its first 10000 commits
                cloningThread = Thread(target=self.cloneRepoThread, args=(repoUrl,))
                cloningThread.start()
                # timeout after 30 minutes if the cloning process is stuck
                cloningThread.join(timeout=1800)
                if cloningThread.is_alive():
                    cloningThread.terminate()
                    raise Exception(f"Failed to clone in 30 minutes")
                
                clonedRepo = GitRepo("temp_repo")
                try:
                    for commit in clonedRepo.iter_commits(paths=["*.yaml", "*.yml"], max_count=10000):
                        try:
                            dbCommit = self.instance.commitController.getCommit(f"{ghRepoUrl}/commits/{commit.hexsha}")
                            if dbCommit is not None:
                                continue
                        except mariadbError as e:
                            self.logger.error(e)
                            continue
                        try:
                            dataForCommit = self.getDataForCommit(commit, ghRepoUrl, clonedRepo)
                        except Exception as e:
                            self.logger.error(e)
                            continue
                        # skip commits that do not modify any YAML files
                        if len(dataForCommit['filePaths']) == 0:
                            continue
                        if repo.stopStage == 'keywords':
                            repo.stopStage = 'yaml'
                        self.checkCommitForKeywords(dataForCommit, repo)
                    if repo.flag is None:
                        self.instance.repoController.createRepo(repo)
                except:
                    raise
                finally:
                    clonedRepo.close()
            except GithubException as e:
                if e.status == 404:
                    self.logger.info(f"Repository {repoUrl} not found", 2)
                    repo = Repo(None, repoUrl, 'missing', 'keywords', 'No', 'No')
                    self.instance.repoController.createRepo(repo)
                    return
                self.logger.error(f"Failed to process repository {repoUrl}: {e}")
                repo = Repo(None, repoUrl, 'error', 'keywords', 'No', 'No')
                self.instance.repoController.createRepo(repo)
                return
            except Exception as e:
                self.logger.error(f"Failed to process repository {repoUrl}: {e}")
                return  
        except mariadbError as e:
            self.logger.dbError(e)
            return
        finally:
            if os.path.exists("temp_repo"):
                process = Popen(["rm", "-rf", "temp_repo"])
                process.wait()