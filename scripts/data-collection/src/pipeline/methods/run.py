import os
from subprocess import Popen
from usage.checkGhLimits import checkGhLimits

def run(self):
        self.yaml.preserve_quotes = True
        if os.path.exists("temp_repo"):
            process = Popen(["rm", "-rf", "temp_repo"])
            process.wait()
        try:
            awsResources = self.parseResourcesJson()
        except Exception as e:
            self.logger.error(e)
        for resource in awsResources:
            try:
                repos = self.extractRepoForResource(resource)
                for repo in repos:
                    checkGhLimits(self.github, 3, self.logger)
                    self.handleRepoForCommit(repo)
            except Exception as e:
                self.logger.error(e)
                continue
        self.instance.db.close()