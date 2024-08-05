from usage.initialization import Initialization
from usage.logger.logger import Logger
from models.plotElement import PlotElement
from usage.ghAuth import GhAuth

import os
import json

if __name__ == '__main__':
    logger = Logger()
    instance = Initialization(logger)
    github = GhAuth(logger)

    effects = [(1, "awareness"), (2, "increase"), (3, "save"), (4, "unrelated")]
    actions = [(1, "alert"), (2, "change"), (3, "test")]
    properties = [(1, "area"), (2, "billing_mode"), (3, "cluster"), (4, "cpu"), (5, "domain"), (6, "feature"), (7, "instance"), (8, "nat"), (9, "networking"), (10, "policy"), (11, "provider"), (12, "ram"), (13, "storage"), (14, "vpn"), (15, "logging"), (16, "permissions")]
    
    if not os.path.exists("output"):
        os.makedirs("output")
    if not os.path.exists("output/before_consolidation"):
        os.makedirs("output/before_consolidation")
    if not os.path.exists("output/after_consolidation"):
        os.makedirs("output/after_consolidation")

    tables = ["commits_alex", "commits_allia", "commits_nicu", "consolidation_alex", "consolidation_allia", "consolidation_nicu"]

    for (indexTables, table) in enumerate(tables):
        results = []
        plotElements = instance.effectController.getAllEffects(table)

        for (index, plotElement) in enumerate(plotElements):
            # get message from commit github
            repoName = plotElement.url[0].split("/")[3] + "/" + plotElement.url[0].split("/")[4]
            try: 
                repo = github.get_repo(repoName)
                commitId = plotElement.url[0].split("/")[6]
                commit = repo.get_commit(commitId)
                plotElement.message = commit.commit.message
            except Exception as e:
                print(f"Failed to get commit {commitId} from {repoName}: {e}")
                plotElement.message = "ERROR: Failed to get commit message"
            instance.actionController.getActionsOfCommit(plotElement, table)
            instance.propertyController.getPropertiesOfCommit(plotElement, table)
            results.append(plotElement.toDict())
            print(f"Processed {index + 1}/{len(plotElements)} commits from {table}")

        if indexTables < 3:
            with open(f'output/before_consolidation/{table.split("_")[1]}.json', 'w') as file:
                json.dump(results, file, indent=2)
        else:
            with open(f'output/after_consolidation/{table.split("_")[1]}.json', 'w') as file:
                json.dump(results, file, indent=2)