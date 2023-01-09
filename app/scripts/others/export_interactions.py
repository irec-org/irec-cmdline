from os.path import dirname, realpath, sep, pardir
import os
import yaml
os.chdir(dirname(realpath(__file__)) + sep + pardir + sep + pardir + sep)
import argparse
from mlflow.tracking import MlflowClient

from irec.connector import utils
import argparse
import pickle
from datetime import datetime

settings = utils.load_settings(dirname(realpath(__file__)))
parser = argparse.ArgumentParser()

parser.add_argument(
    "--evaluation_policy", default=settings["defaults"]["evaluation_policy"]
)
parser.add_argument(
    "--dataset_loaders", nargs="*", default=[settings["defaults"]["dataset_loader"]]
)
parser.add_argument("--agents", nargs="*", default=[settings["defaults"]["agent"]])

args = parser.parse_args()

dataset_agents_parameters = yaml.load(
    open("./settings/dataset_agents.yaml"), Loader=yaml.SafeLoader
)

settings["defaults"]["evaluation_policy"] = args.evaluation_policy

export_dir = "./data/exported_data"

if not os.path.isdir(export_dir):
    os.makedirs(export_dir)

for dataset_loader_name in args.dataset_loaders:
    settings["defaults"]["dataset_loader"] = dataset_loader_name

    for agent_name in args.agents:

        settings["defaults"]["agent"] = agent_name
        settings["agents"][agent_name] = dataset_agents_parameters[
            dataset_loader_name
        ][agent_name]

        run = utils.get_agent_run(settings)

        if run is None:
            print("Could not find agent run")
            continue

        client = MlflowClient()
        artifact_path = client.download_artifacts(run.info.run_id, "interactions.pickle")
        with open(artifact_path, "rb") as f:
            interactions = pickle.load(f)
        
        file_name = f"{dataset_loader_name}_{agent_name}_{args.evaluation_policy}_{datetime.now()}"

        print(f"\nExporting {file_name} to {export_dir}...", end="\r")

        with open(f"{export_dir}/{file_name}", "wb") as f:
            pickle.dump(interactions, f)

        print(f"Exporting {file_name} to {export_dir}... Done")
