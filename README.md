# Supplementary Material

This repository contains the supplementary material for the paper entitled:

**Mining for Cost Awareness in Cloud Computing: A Study of AWS CloudFormation and Developer Practices**

The supplementary material includes:
- script to support raw data collection and cached versions of data generated during the raw data collection;
- the compiled dataset containing evidence of cost awareness in commits of cloud-based software repositories, and associated information.

**Replication disclaimers:**
> (1) We note that running the provided data collection script from scratch will result in variations in the output files since projects have evolved and some projects may have been deleted or made private.
>
> (2) The provided script aid the collection of the raw data (i.e., candidate commits) to be analyzed for evidence of cost awareness (the raw dataset can be imported from the sql file [rawdataset.sql](rawdataset.sql)). The next step to generate the provided [dataset.json](dataset.json) (i.e., filtering of relevant commits and issues and coding) was manual. Therefore, there is no code to automate this final steps and we only provide the dataset and associated information (i.e., [codes.json](codes.json)). You can also find all cached repositories that were verified in [repositories.txt](repositories.txt).

## Database Structure

> 1. **cloudformation** database
>    1. **repos** table | contains the repositories that were checked
>        1. **id** entry | auto-incremented id when adding a new repository
>        2. **url** entry | the url of the repository
>        3. **flag** entry | the repository status
>            1. **none** flag | it is not a repository that changes AWS CF files
>            2. **aws** flag | it is a repository that changes AWS CF files
>            3. **error** flag | it encountered an error while trying to check the repository
>            4. **skipped** flag | the repository is bigger than 5GB
>            5. **missing** flag | the repository could not be found
>        4. **stop_stage** entry | what was found in the repository
>            1. **yaml** stop stage | the repository contains YAML files
>            2. **aws** stop stage | the repository contains AWS CloudFormation files
>        5. **truncated_1k** entry | the repository has more than 1.000 commits
>        6. **truncated_10k** entry | the repository has more than 10.000 commits
>    2. **commits** table | contains the commits that changes AWS CF files
>        1. **id** entry | auto-incremented id when adding a new commit
>        2. **repo_id** entry | the id of the repository
>        3. **url** entry | the url of the commit
>        4. **hash** entry | the hash of the commit
>        5. **has_non_template** entry | the AWS CF file found is not a template
>    3. **keywords** table | contains the list of keywords that were searched
>        1. **id** entry | auto-incremented id when adding a new keyword
>        2. **name** entry | the keyword
>            1. **bill** keyword
>            2. **cheap** keyword
>            3. **cost** keyword
>            4. **efficient** keyword
>            5. **expens** keyword
>            6. **pay** keyword
>    4. **keywords_commits** table | relationship between the commits and keywords that were present in the commit message
>        1. **keyword_id** entry | the id of the keyword
>        2. **commit_id** entry | the id of the commit

## Contents

### **`scripts/`**

- **`Dockerfile`**, **`docker-compose.yml`**, **`.env.example`** | Files to build and start a Docker container with a Python instance and a MariaDB instance and all necessary dependencies (see `.env.example`).
- **`data-collection/`** | Python Script to automate the raw data retrieval.
- **`data-collection/src/usage/logger/logs`** | The logs provided by the Python Script.
- **`data/`** | The necessary files to create the MariaDB instance.

Running script:
> 1. Install [Docker Engine](https://docs.docker.com/engine/install/)
> 2. In the terminal/cmd
>    1. Navigate to the folder `scripts/`
>    2. Rename **`.env.example`** to **`.env`**
>    3. Change the GitHub token from **`.env`**
>    4. Run `docker compose up`
> 3. You can find all extracted commits and repositories by connecting to the database with the information provided in the **`.env`** file using an administation tool like HeidiSQL (you can do this while the script is running and see the database updating live)
>    1. Navigate in the "cloudformation" database
>    2. To see the repositories that were checked you can enter the "repos" table
>    3. To see the commits that contained relevant keywords you can enter the "commits" table

### **`dataset.json`**

- **Content**: Evidence of cost awareness in commits and issues of cloud-based software repositories.
- **Format**: List of entries in JSON.
- **Size**: 262 entries.
- **Collection period**: May 2024.
- **Entry fields** ([JSON Schema](https://json-schema.org/)):
  ```json
  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "DatasetInfo",
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "description": "Type of entry ('commit' or 'issue')."
        },
        "url": {
            "type": "string",
            "description": "Link to the commit or issue."
        },
        "content": {
            "type": "object",
            "description": "Commit message or issue content.",
            "properties": {
              "message": {
                  "type": "string",
                  "description": "Commit message (only for commit entries)."
              },
              "title": {
                  "type": "string",
                  "description": "Issue title (only for issue entries)."
              },
              "body": {
                  "type": "string",
                  "description": "Issue body (only for issue entries)."
              },
              "comments": {
                  "type": "array",
                  "description": "Issue comments (only for issue entries).",
                  "items": {
                      "type": "string",
                      "description": "Issue comment"
                  }
              },
            }
        },
        "codes": {
            "type": "array",
            "items": {
                "type": "string",
                "description": "Cost-related code assigned to the commit message (see Section 'Codes')."
            }
        }
    }
  }
  ```
- Example entry:
  ```json
  {
    "type": "commit",
    "url": "https://github.com/zaro0508/organizations-infra/commit/1a35ef50ccf357c8319a60fd1c95bd6fd412517b",
    "content": {
      "message": "[IT-1046] Deploy cost reports lambda with S3 notifications\n\nAdd the cost report lambda to the budgets tasks, and trigger\nthe lambda with S3 notifications for files written by AWS Billing.\n\nDepends on: Sage-Bionetworks-IT/lambda-cost-reports#4"
    },
    "codes": [
      "awareness",
      "track",
      "report"
    ]
  },
  ```

### **`codes.json`**

- **Content**: Description of the codes identified during the study.
- **Format**: List of entries in JSON.
- **Size**: 24 entries.
- **Collection period**: May 2024.
- **Entry fields** ([JSON Schema](https://json-schema.org/)):
  ```json
  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Code",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Name of the code."
        },
        "description": {
            "type": "string",
            "description": "Desription of the code."
        }
    }
  }
  ```
- Example entry:
  ```json
  {
    "name": "save",
    "description": "denotes mentioned changes explicitly made to save costs."
  },
  ```