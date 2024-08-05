import os
from ruamel.yaml import YAML
from usage.initialization import Initialization
from usage.ghAuth import GhAuth
from usage.logger.logger import Logger
from pipeline.methods import *

class Pipeline:
    run = run
    cloneRepoThread = cloneRepoThread
    isAwsFileTemplate = isAwsFileTemplate
    checkoutCommitFiles = checkoutCommitFiles
    postNewCommit = postNewCommit
    checkCommitForAws = checkCommitForAws
    checkCommitForKeywords = checkCommitForKeywords
    getDataForCommit = getDataForCommit
    handleRepoForCommit = handleRepoForCommit
    parseResourcesJson = parseResourcesJson
    extractRepoForResource = extractRepoForResource
    
    def __init__(self):
        self.logger = Logger()
        self.instance = Initialization(self.logger)
        self.github = GhAuth(self.logger)
        self.keywords = [(1, 'bill'), (2, 'cheap'), (3, 'cost'), (4, 'efficient'), (5, 'expens'), (6, 'pay')]
        self.templates = []
        for template in os.listdir("templates"):
            with open(f"templates/{template}", "r") as file:
                self.templates.append(file.read())
        self.yaml = YAML()
        self.run()
