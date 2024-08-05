import json

def parseResourcesJson(self) -> list:
    try:
        with open("usage/awsResources.json", "r") as file:
            return json.load(file)['AwsResources']
    except Exception as e:
        raise Exception(f"Could not parse AWS resources JSON: {e}")
