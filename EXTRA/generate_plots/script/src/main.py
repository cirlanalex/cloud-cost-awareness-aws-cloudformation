from usage.initialization import Initialization
from usage.logger.logger import Logger
from models.plotElement import PlotElement

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import upsetplot as up
import matplotlib.lines as mlines
import json

if __name__ == '__main__':
    logger = Logger()
    instance = Initialization(logger)

    # FIRST PLOT
    effects = [(1, "awareness"), (2, "increase"), (3, "save")] #, (4, "unrelated")
    actions = [(1, "change"), (2, "test"), (3, "track")]
    properties = [(1, "alert"), (2, "area"), (3, "billing_mode"), (4, "cluster"), (5, "cpu"), (6, "domain"), (7, "feature"), (8, "instance"), (9, "logging"), (10, "nat"), (11, "networking"), (12, "policy"), (13, "provider"), (14, "ram"), (15, "report"), (16, "service"), (17, "storage"), (18, "vpn")]

    results = []

    instanceCommitUrls = []
    instanteRepoUrls = []
    networkingCommitUrls = []
    networkingRepoUrls = []

    for effect in effects:
        repos, commits = instance.resultEffectController.getEffects(effect[0])
        print(f"There are {len(set(commits))} commits and {len(set(repos))} unique repositories with the effect {effect[1]}")
        results.append((effect[1], len(set(commits)), len(set(repos))))
    
    for action in actions:
        repos, commits = instance.resultActionController.getActions(action[0])
        print(f"There are {len(set(commits))} commits and {len(set(repos))} unique repositories with the action {action[1]}")
        results.append((action[1], len(set(commits)), len(set(repos))))
    
    for property in properties:
        repos, commits = instance.resultPropertyController.getProperties(property[0])
        print(f"There are {len(set(commits))} commits and {len(set(repos))} unique repositories with the property {property[1]}")
        results.append((property[1], len(set(commits)), len(set(repos))))
        if property[1] == "networking" or property[1] == "nat" or property[1] == "vpn" or property[1] == "domain":
            for commit in commits:
                networkingCommitUrls.append(commit)
            for repo in repos:
                networkingRepoUrls.append(repo)
        if property[1] == "instance" or property[1] == "cpu" or property[1] == "ram":
            for commit in commits:
                instanceCommitUrls.append(commit)
            for repo in repos:
                instanteRepoUrls.append(repo)
        
    print(f"There are {len(set(networkingCommitUrls))} commits and {len(set(networkingRepoUrls))} unique repositories with the networking properties")
    print(f"There are {len(set(instanceCommitUrls))} commits and {len(set(instanteRepoUrls))} unique repositories with the instance properties")

    results[13] = ("instance", len(set(instanceCommitUrls)), len(set(instanteRepoUrls)))
    results[16] = ("networking", len(set(networkingCommitUrls)), len(set(networkingRepoUrls)))
    
    # Grouped barchart of total and unique repositories per type with 2 bars per type and order by total
    df = pd.DataFrame(results, columns=["Label", "Commits", "Repositories"])
    df = df.sort_values(by='Commits', ascending=False)
    df = df.melt('Label', var_name='Metric', value_name='Count')
    sns.set_theme(style="whitegrid", rc={'figure.figsize':(15, 15)}, palette="pastel")
    plot = sns.barplot(x='Label', y='Count', hue='Metric', data=df)

    # change text size of the labels
    for item in plot.get_xticklabels():
        item.set_fontsize(15)
    for item in plot.get_yticklabels():
        item.set_fontsize(15)

    # change legend text size
    for item in plot.get_legend().get_texts():
        item.set_fontsize(15)
    # change legend title size
    plot.get_legend().get_title().set_fontsize('15')

     # for y-axis name, change the font size
    plot.set_ylabel("Count", fontsize=15)

    # Adding the values on top of each bar
    for p in plot.patches:
        if p.get_height() > 0:  # Only annotate bars with a height greater than 0
            plot.annotate(format(p.get_height(), '.0f'), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', 
                        xytext = (0, 9), 
                        textcoords = 'offset points', fontsize=13)
            
    # change color of label text based on action, effect or property(unordered)
    for i in range(0, len(results)):
        if plot.get_xticklabels()[i].get_text() in ["change", "test", "track"]:
            plot.get_xticklabels()[i].set_color("blue")
        elif plot.get_xticklabels()[i].get_text() in ["awareness", "increase", "save"]:
            plot.get_xticklabels()[i].set_color("green")
        else:
            plot.get_xticklabels()[i].set_color("red")

    # Create custom legend elements
    custom_lines = [
        mlines.Line2D([], [], color='green', marker='o', linestyle='None', markersize=10, label='Effect'),
        mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=10, label='Action'),
        mlines.Line2D([], [], color='red', marker='o', linestyle='None', markersize=10, label='Property')
    ]

    # Add the custom legend
    custom_legend = plt.legend(handles=custom_lines, loc='upper right', bbox_to_anchor=(1, 0.855), title='Label Type', title_fontsize='15', fontsize='15')
    plt.gca().add_artist(custom_legend)

    # Add the default legend
    plt.legend(loc='upper right', title='Metric', title_fontsize='15', fontsize='15')
    
    # add the default legend of Metric

    # add legend for colors of the labels
    # newLegend = plt.legend(title="Label type", title_fontsize='15', fontsize='15', loc=4, labels=['Action', 'Effect', 'Property'])

    plt.xticks(rotation=45)

    plt.gcf().set_size_inches(19.20, 10.80)

    plt.savefig("output/AWSFrequencyPlot.png")

    plt.show()

    # SECOND PLOT (UpSet plot)

    results = []

    plotElements = instance.effectController.getAllEffects()

    for plotElement in plotElements:
        instance.actionController.getActionsOfCommit(plotElement)
        instance.propertyController.getPropertiesOfCommit(plotElement)
        results.append(plotElement.getResult())
    
    # count all combinations of effects, actions and properties

    df = pd.DataFrame(results, columns=["awareness", "increase", "save", "change", "test", "track", "alert", "area", "billing_mode", "cluster", "cpu", "domain", "feature", "instance", "logging", "nat", "networking", "policy", "provider", "ram", "report", "service", "storage", "vpn"])
    df = df.groupby(df.columns.tolist()).size().reset_index().rename(columns={0: 'count'})
    # order the columns by the count of the combinations
    df = df.sort_values(by='count', ascending=False)


    newResults = []
    count = []

    for df_row in df.iterrows():
        # push only the True values to the newResults list
        newResults.append([df.columns[i] for i in range(0, len(df_row[1]) - 1) if df_row[1][i] == True])
        count.append(df_row[1][-1])
    
    # create the UpSet plot
    upsetSorted = up.from_memberships(newResults, data=count)

    upset = up.UpSet(upsetSorted, orientation='horizontal', show_counts=True, sort_by='cardinality', sort_categories_by='-cardinality', facecolor="darkblue", element_size=30)

    plot = upset.plot()

    matrix_ax = plot['matrix']
    shading_ax = plot['shading']
    totals_ax = plot['totals']
    intersections_ax = plot['intersections']

    for item in matrix_ax.get_xticklabels():
        item.set_fontsize(15)
    for item in matrix_ax.get_yticklabels():
        item.set_fontsize(15)
    
    for item in intersections_ax.get_xticklabels():
        item.set_fontsize(15)
    for item in intersections_ax.get_yticklabels():
        item.set_fontsize(15)
    
    # for each annotation in the matrix, change the font size
    for annotation in totals_ax.texts:
        annotation.set_fontsize(15)
    
    for annotation in intersections_ax.texts:
        annotation.set_fontsize(15)

    # for y-axis name from intersections, change the font size
    intersections_ax.set_ylabel("Intersection size", fontsize=15)

    plt.gcf().set_size_inches(19.20, 10.80)
        
    plt.savefig("output/AWSUpsetPlot.png")

    plt.show()

    # reset plt
    plt.clf()

    # FIRST PLOT WITH THE COMMON PROPERTIES

    results = []

    instanceCommitUrls = []
    instanteRepoUrls = []
    networkingCommitUrls = []
    networkingRepoUrls = []

    for effect in effects:
        repos, commits = instance.resultEffectController.getEffects(effect[0])
        print(f"There are {len(set(commits))} commits and {len(set(repos))} unique repositories with the effect {effect[1]}")
        results.append((effect[1], len(set(commits))))
    
    for property in properties:
        repos, commits = instance.resultPropertyController.getProperties(property[0])
        print(f"There are {len(set(commits))} commits and {len(set(repos))} unique repositories with the property {property[1]}")
        if property[1] != "cpu" and property[1] != "logging" and property[1] != "nat" and property[1] != "ram" and property[1] != "report" and property[1] != "service" and property[1] != "vpn":
            results.append((property[1], len(set(commits))))
        if property[1] == "networking" or property[1] == "nat" or property[1] == "vpn" or property[1] == "domain":
            for commit in commits:
                networkingCommitUrls.append(commit)
            for repo in repos:
                networkingRepoUrls.append(repo)
        if property[1] == "instance" or property[1] == "cpu" or property[1] == "ram":
            for commit in commits:
                instanceCommitUrls.append(commit)
            for repo in repos:
                instanteRepoUrls.append(repo)
        
    print(f"There are {len(set(networkingCommitUrls))} commits and {len(set(networkingRepoUrls))} unique repositories with the networking properties")
    print(f"There are {len(set(instanceCommitUrls))} commits and {len(set(instanteRepoUrls))} unique repositories with the instance properties")

    results[9] = ("instance", len(set(instanceCommitUrls)))
    results[10] = ("networking", len(set(networkingCommitUrls)))

    plt.subplot(1, 2, 1)
    
    # Grouped barchart of total and unique repositories per type with 2 bars per type and order by total
    df = pd.DataFrame(results, columns=["Label", "AWS CF Commits"])
    df = df.sort_values(by='AWS CF Commits', ascending=False)
    df = df.melt('Label', var_name='Metric', value_name='Count')
    sns.set_theme(style="whitegrid", rc={'figure.figsize':(15, 15)}, palette="pastel")
    plot = sns.barplot(x='Label', y='Count', hue='Metric', data=df)

    # set the title of the plot
    plt.title("AWS CloudFormation", fontsize=15)

    # change text size of the labels
    for item in plot.get_xticklabels():
        item.set_fontsize(15)
    for item in plot.get_yticklabels():
        item.set_fontsize(15)

    # change legend text size
    for item in plot.get_legend().get_texts():
        item.set_fontsize(15)
    # change legend title size
    plot.get_legend().get_title().set_fontsize('15')

     # for y-axis name, change the font size
    plot.set_ylabel("Count", fontsize=15)

    # Adding the values on top of each bar
    for p in plot.patches:
        if p.get_height() > 0:  # Only annotate bars with a height greater than 0
            plot.annotate(format(p.get_height(), '.0f'), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', 
                        xytext = (0, 9), 
                        textcoords = 'offset points', fontsize=13)
            
    # change color of label text based on action, effect or property(unordered)
    for i in range(0, len(results)):
        if plot.get_xticklabels()[i].get_text() in ["awareness", "increase", "save"]:
            plot.get_xticklabels()[i].set_color("green")
        else:
            plot.get_xticklabels()[i].set_color("red")

    # Create custom legend elements
    custom_lines = [
        mlines.Line2D([], [], color='green', marker='o', linestyle='None', markersize=10, label='Effect'),
        mlines.Line2D([], [], color='red', marker='o', linestyle='None', markersize=10, label='Property')
    ]

    # Add the custom legend
    custom_legend = plt.legend(handles=custom_lines, loc='upper right', bbox_to_anchor=(1, 0.89), title='Label Type', title_fontsize='15', fontsize='15')
    plt.gca().add_artist(custom_legend)

    # Add the default legend
    plt.legend(loc='upper right', title='Metric', title_fontsize='15', fontsize='15')

    plt.xticks(rotation=45)
    # plt.show()

    # TERRAFORM COMMON LABELS

    # load json file dataset from usage
    with open('usage/dataset.json') as f:
        data = json.load(f)

    count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    commonEffects = [(1, "awareness"), (2, "increase"), (3, "saving")] #, (4, "unrelated")
    commonProperties = [(1, "alert"), (2, "area"), (3, "billing_mode"), (4, "cluster"), (6, "domain"), (7, "feature"), (8, "instance"), (11, "networking"), (12, "policy"), (13, "provider"), (17, "storage")]
    
    relevantCommitsTerraform = 0
    relevantCommitsAWS = 262

    for entry in data:
        if entry["type"] == "commit":
            relevantCommitsTerraform += 1

    for (index, effect) in enumerate(commonEffects):
        for entry in data:
            if entry["type"] == "commit":
                for code in entry["codes"]:
                    if code == effect[1]:
                        count[index] += 1
    
    for (index, property) in enumerate(commonProperties):
        for entry in data:
            if entry["type"] == "commit":
                for code in entry["codes"]:
                    if code == property[1]:
                        count[index+3] += 1

    newCount = []
    
    for result in count:
        newCount.append(result)
        # newCount.append(math.floor(result / relevantCommitsTerraform * 100))

    results = []

    for (index, effect) in enumerate(effects):
        results.append((effect[1], newCount[index]))
    
    for (index, property) in enumerate(commonProperties):
        results.append((property[1], newCount[index+3]))

    plt.subplot(1, 2, 2)

    # Grouped barchart of total and unique repositories per type with 2 bars per type and order by total
    df = pd.DataFrame(results, columns=["Label", "Terraform Commits"])
    df = df.sort_values(by='Terraform Commits', ascending=False)
    df = df.melt('Label', var_name='Metric', value_name='Count')
    sns.set_theme(style="whitegrid", rc={'figure.figsize':(15, 15)}, palette="pastel")
    # Define pastel red color
    pastel_red = "#AD88C6"
    plot = sns.barplot(x='Label', y='Count', hue='Metric', data=df, palette=[pastel_red])

    # set the title of the plot
    plt.title("Terraform", fontsize=15)

    # change text size of the labels
    for item in plot.get_xticklabels():
        item.set_fontsize(15)
    for item in plot.get_yticklabels():
        item.set_fontsize(15)

    # change legend text size
    for item in plot.get_legend().get_texts():
        item.set_fontsize(15)
    # change legend title size
    plot.get_legend().get_title().set_fontsize('15')

     # for y-axis name, change the font size
    plot.set_ylabel("Count", fontsize=15)

    # Adding the values on top of each bar
    for p in plot.patches:
        if p.get_height() > 0:  # Only annotate bars with a height greater than 0
            plot.annotate(format(p.get_height(), '.0f'), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', 
                        xytext = (0, 9), 
                        textcoords = 'offset points', fontsize=13)
            
    # change color of label text based on action, effect or property(unordered)
    for i in range(0, len(results)):
        if plot.get_xticklabels()[i].get_text() in ["awareness", "increase", "save"]:
            plot.get_xticklabels()[i].set_color("green")
        else:
            plot.get_xticklabels()[i].set_color("red")

    # Create custom legend elements
    custom_lines = [
        mlines.Line2D([], [], color='green', marker='o', linestyle='None', markersize=10, label='Effect'),
        mlines.Line2D([], [], color='red', marker='o', linestyle='None', markersize=10, label='Property')
    ]

    # Add the custom legend
    custom_legend = plt.legend(handles=custom_lines, loc='upper right', bbox_to_anchor=(1, 0.89), title='Label Type', title_fontsize='15', fontsize='15')
    plt.gca().add_artist(custom_legend)

    # Add the default legend
    plt.legend(loc='upper right', title='Metric', title_fontsize='15', fontsize='15')

    plt.xticks(rotation=45)

    plt.gcf().set_size_inches(19.20, 10.80)

    plt.savefig("output/AWSvsTerraformFrequencyPlot.png")

    plt.show()

    # SECOND PLOT (UpSet plot) WITH THE COMMON PROPERTIES

    results = []

    plotElements = instance.effectController.getAllEffects()

    for plotElement in plotElements:
        instance.actionController.getActionsOfCommit(plotElement)
        instance.propertyController.getPropertiesOfCommit(plotElement)
        results.append(plotElement.getCommonResult())
    
    # count all combinations of effects, actions and properties

    df = pd.DataFrame(results, columns=["awareness", "increase", "save", "alert", "area", "billing_mode", "cluster", "domain", "feature", "instance", "networking", "policy", "provider", "storage"])
    df = df.groupby(df.columns.tolist()).size().reset_index().rename(columns={0: 'count'})
    # order the columns by the count of the combinations
    df = df.sort_values(by='count', ascending=False)


    newResults = []
    count = []

    for df_row in df.iterrows():
        # push only the True values to the newResults list
        newResults.append([df.columns[i] for i in range(0, len(df_row[1]) - 1) if df_row[1][i] == True])
        count.append(df_row[1][-1])
    
    # create the UpSet plot
    upsetSorted = up.from_memberships(newResults, data=count)

    upset = up.UpSet(upsetSorted, orientation='horizontal', show_counts=True, sort_by='cardinality', sort_categories_by='-cardinality', facecolor="darkblue", element_size=30)

    plot = upset.plot()

    # set the title of the plot
    plt.title("AWS CloudFormation", fontsize=15)

    matrix_ax = plot['matrix']
    shading_ax = plot['shading']
    totals_ax = plot['totals']
    intersections_ax = plot['intersections']

    for item in matrix_ax.get_xticklabels():
        item.set_fontsize(15)
    for item in matrix_ax.get_yticklabels():
        item.set_fontsize(15)
    
    for item in intersections_ax.get_xticklabels():
        item.set_fontsize(15)
    for item in intersections_ax.get_yticklabels():
        item.set_fontsize(15)
    
    # for each annotation in the matrix, change the font size
    for annotation in totals_ax.texts:
        annotation.set_fontsize(15)
    
    for annotation in intersections_ax.texts:
        annotation.set_fontsize(15)

    # for y-axis name from intersections, change the font size
    intersections_ax.set_ylabel("Intersection size", fontsize=15)

    plt.gcf().set_size_inches(19.20, 10.80)

    plt.savefig("output/AWSCommonUpsetPlot.png")

    plt.show()

    # SECOND PLOT (UpSet plot) WITH THE COMMON PROPERTIES FOR TERRAFORM

    results = []

    for entry in data:
        if entry["type"] == "commit":
            plotElement = PlotElement(entry["url"])
            for code in entry["codes"]:
                if code == "awareness":
                    plotElement.awareness = True
                elif code == "increase":
                    plotElement.increase = True
                elif code == "saving":
                    plotElement.save = True
                elif code == "alert":
                    plotElement.alert = True
                elif code == "area":
                    plotElement.area = True
                elif code == "billing_mode":
                    plotElement.billing_mode = True
                elif code == "cluster":
                    plotElement.cluster = True
                elif code == "domain":
                    plotElement.domain = True
                elif code == "feature":
                    plotElement.feature = True
                elif code == "instance":
                    plotElement.instance = True
                elif code == "networking":
                    plotElement.networking = True
                elif code == "policy":
                    plotElement.policy = True
                elif code == "provider":
                    plotElement.provider = True
                elif code == "storage":
                    plotElement.storage = True
            results.append(plotElement.getCommonResult())
    
    # count all combinations of effects, actions and properties

    df = pd.DataFrame(results, columns=["awareness", "increase", "save", "alert", "area", "billing_mode", "cluster", "domain", "feature", "instance", "networking", "policy", "provider", "storage"])
    df = df.groupby(df.columns.tolist()).size().reset_index().rename(columns={0: 'count'})
    # order the columns by the count of the combinations
    df = df.sort_values(by='count', ascending=False)


    newResults = []
    count = []

    for df_row in df.iterrows():
        # push only the True values to the newResults list
        newResults.append([df.columns[i] for i in range(0, len(df_row[1]) - 1) if df_row[1][i] == True])
        count.append(df_row[1][-1])
    
    # create the UpSet plot
    upsetSorted = up.from_memberships(newResults, data=count)

    upset = up.UpSet(upsetSorted, orientation='horizontal', show_counts=True, sort_by='cardinality', sort_categories_by='-cardinality', facecolor="purple", element_size=30)

    plot = upset.plot()

    # set the title of the plot
    plt.title("Terraform", fontsize=15)

    matrix_ax = plot['matrix']
    shading_ax = plot['shading']
    totals_ax = plot['totals']
    intersections_ax = plot['intersections']

    for item in matrix_ax.get_xticklabels():
        item.set_fontsize(15)
    for item in matrix_ax.get_yticklabels():
        item.set_fontsize(15)
    
    for item in intersections_ax.get_xticklabels():
        item.set_fontsize(15)
    for item in intersections_ax.get_yticklabels():
        item.set_fontsize(15)
    
    # for each annotation in the matrix, change the font size
    for annotation in totals_ax.texts:
        annotation.set_fontsize(15)
    
    for annotation in intersections_ax.texts:
        annotation.set_fontsize(15)

    # for y-axis name from intersections, change the font size
    intersections_ax.set_ylabel("Intersection size", fontsize=15)

    plt.gcf().set_size_inches(19.20, 10.80)
        
    plt.savefig("output/TerraformCommonUpsetPlot.png")

    plt.show()