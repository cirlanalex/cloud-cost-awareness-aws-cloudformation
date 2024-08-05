from usage.checkGhLimits import checkGhLimits
from time import sleep

def extractRepoForResource(self, resource: object) -> list:
    try:
        self.logger.info(f"Extracting repositories for resource {resource['name']}")
        repos = []
        checkGhLimits(self.github, 2, self.logger)
        searches = self.github.search_code(f"extension:yaml OR extension:yml {resource['name']}")
        sleep(0.3)
        if searches.totalCount == 0:
            raise Exception(f"No repositories found for resource {resource['name']}")
        for file in searches:
            repo = f"https://api.github.com/repos/{file.repository.full_name}"
            if repo not in repos:
                repos.append(repo)
            sleep(0.3)
        if searches.totalCount >= 1000:
            self.logger.info(f"Resource {resource['name']} has more than 1000 repositories", 1)
            checkGhLimits(self.github, resource['resourceTypes'].__len__() + 1, self.logger)
            for type in resource['resourceTypes']:
                self.logger.info(f"Extracting repositories for resource type {type}", 2)
                searchType = self.github.search_code(f"extension:yaml OR extension:yml {type}")
                sleep(0.3)
                if searchType.totalCount == 0:
                    continue
                for file in searchType:
                    repo = f"https://api.github.com/repos/{file.repository.full_name}"
                    if repo not in repos:
                        repos.append(repo)
                    sleep(0.3)
                if searchType.totalCount >= 1000:
                    self.logger.info(f"Resource type {type} has more than 1000 repositories", 2)
        return repos
            
    except Exception as e:
        raise Exception(f"Could not extract repo for resource: {e}")