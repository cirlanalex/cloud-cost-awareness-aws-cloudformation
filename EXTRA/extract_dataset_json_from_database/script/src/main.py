from usage.initialization import Initialization
from usage.logger.logger import Logger
from models.plotElement import PlotElement
from usage.ghAuth import GhAuth

import json

if __name__ == '__main__':
    logger = Logger()
    instance = Initialization(logger)
    github = GhAuth(logger)

    # FIRST PLOT
    effects = [(1, "awareness"), (2, "increase"), (3, "save"), (4, "unrelated")]
    actions = [(1, "change"), (2, "test"), (3, "track")]
    properties = [(1, "alert"), (2, "area"), (3, "billing_mode"), (4, "cluster"), (5, "cpu"), (6, "domain"), (7, "feature"), (8, "instance"), (9, "logging"), (10, "nat"), (11, "networking"), (12, "policy"), (13, "provider"), (14, "ram"), (15, "report"), (16, "service"), (17, "storage"), (18, "vpn")]

    # SECOND PLOT (UpSet plot)

    results = []

    plotElements = instance.effectController.getAllEffects()

    for (index, plotElement) in enumerate(plotElements):
        # get message from commit github
        repoName = plotElement.url[0].split("/")[3] + "/" + plotElement.url[0].split("/")[4]
        repo = github.get_repo(repoName)
        commitId = plotElement.url[0].split("/")[6]
        commit = repo.get_commit(commitId)
        plotElement.message = commit.commit.message
        instance.actionController.getActionsOfCommit(plotElement)
        instance.propertyController.getPropertiesOfCommit(plotElement)
        results.append(plotElement.toDict())
        print(f"Processed {index + 1}/{len(plotElements)} commits")

    with open("output/dataset.json", "w") as file:
        json.dump(results, file, indent=2)