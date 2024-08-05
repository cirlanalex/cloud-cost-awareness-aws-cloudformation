# EXTRA FILES AND SCRIPTS

**Here is all the documentation needed for the extra scripts or files that are in this folder**

## Contents
>1. [full_database.sql](full_database.sql) | The database that is used for the majority of scripts inside this folder
>2. [extract_dataset_json_from_database](extract_dataset_json_from_database) | Generate the file dataset.json from the database
>    1. [.env.example](extract_dataset_json_from_database/.env.example) | rename to ".env" and complete with the database details and the GitHub Token
>3. [compute_consensus_level](compute_consensus_level) | Compute the consensus level between each team member before consolidation and after consolidation
>    1. [alpha.txt](compute_consensus_level/alpha.txt) | You can see the results in this file
>    2. [.env.example](compute_consensus_level/.env.example) | rename to ".env" and complete with the database details
>4. [generate_plots](generate_plots) | You can generate all plots used in the paper(AWS CF Frequency Plot + AWS CF UpSet Plot + AWS CF vs Terraform Frequency Plots + AWS CF vs Terraform UpSet Plots)
>    1. [.env.example](generate_plots/.env.example) | rename to ".env" and complete with the database details
>    2. [dataset.json](generate_plots/usage/dataset.json) | the Terraform dataset of commits only