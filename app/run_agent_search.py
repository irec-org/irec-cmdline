#!/usr/bin/python3

from os.path import dirname, realpath
import yaml
import os
import argparse
from irec.connector.utils import load_dataset_experiment
from irec.connector import utils
import argparse
from irec.recommendation.hyperoptimization.grid_search import GridSearch

settings = utils.load_settings(dirname(realpath(__file__)))
parser = argparse.ArgumentParser()

parser.add_argument(
    "--evaluation_policy", default=settings["defaults"]["evaluation_policy"]
)
parser.add_argument(
    "--dataset_loaders", nargs="*", default=[settings["defaults"]["dataset_loader"]]
)
parser.add_argument("--agents", nargs="*", default=[settings["defaults"]["agent"]])
parser.add_argument("--tasks", type=int, default=os.cpu_count())
parser.add_argument("--forced_run", action='store_true', default=False)
parser.add_argument("--tunning", default="GridSearch")

utils.load_settings_to_parser(settings, parser)
args = parser.parse_args()
settings = utils.sync_settings_from_args(settings, args)

# agents_search = yaml.load(open("./settings/agents_search.yaml"), Loader=yaml.SafeLoader)
agents_variables = yaml.load(open("./settings/agents_variables.yaml"), Loader=yaml.SafeLoader)
agents_variables = [template for agent_name in args.agents for template in agents_variables[args.tunning] if agent_name in template]

g = GridSearch()
agents_search = g.generate_settings(agents_variables)
settings["defaults"]["evaluation_policy"] = args.evaluation_policy

for dataset_loader_name in args.dataset_loaders:
    settings["defaults"]["dataset_loader"] = dataset_loader_name
    train_dataset, test_dataset, x_validation, y_validation = load_dataset_experiment(settings, validation=True)
    g.execute(x_validation, y_validation, agents_search, settings, args.tasks, args.forced_run)

# utils.run_agent_search(args.agents,args.dataset_loaders,
        # settings, agents_search, args.tasks,args.forced_run)