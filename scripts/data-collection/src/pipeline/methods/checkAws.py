from mariadb import Error as mariadbError
from models.repo import Repo

def checkCommitForAws(self, commit: object, repo: Repo):
        try:
            commit['has_non_template'] = None
            awsFileFound = False
            self.checkoutCommitFiles(commit)
            for filePath in commit['filePaths']:
                try:
                    self.logger.info(f"Checking file {filePath}", 3)
                    fileContent = open(f"temp_repo/{filePath}", "r").read()

                    # check if the file contains AWS marker
                    if "Resources" not in fileContent:
                        continue
                    if "AWS::" not in fileContent:
                        continue

                    # parse the file as YAML
                    yamlContentFiles = self.yaml.load_all(fileContent)
                    awsFileFound = False
                    for yamlFile in yamlContentFiles:
                        # check if the file contains AWS resources
                        if "Resources" in yamlFile:
                            for resource in yamlFile["Resources"].values():
                                if resource["Type"].startswith("AWS::"):
                                    if repo.flag is None:
                                        repo.flag = 'aws'
                                        repo.stopStage = 'aws'
                                    awsFileFound = True
                                    commit['has_non_template'] = "No"
                                    break
                        if awsFileFound:
                            break
                    if awsFileFound:
                        if not self.isAwsFileTemplate(fileContent):
                            self.logger.info(f"File {filePath} from commit {commit['commit_url']} is not a template", 3)
                            commit['has_non_template'] = "Yes"
                            break
                except Exception as e:
                    self.logger.error(f"Could not check file {filePath} from commit {commit['commit_url']}: {e}")
            if commit['has_non_template'] is not None:
                self.postNewCommit(commit, repo)
        except mariadbError as e:
            self.logger.dbError(f"Failed to create commit {commit['commit_url']} with template {commit['has_non_template']}: {e}")
        except Exception as e:
            self.logger.error(f"Failed to process commit {commit['commit_url']}: {e}")