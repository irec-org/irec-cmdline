from os.path import dirname, realpath, sep, pardir
import os
import yaml
os.chdir(dirname(realpath(__file__)) + sep + pardir + sep + pardir + sep)
import argparse

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
parser.add_argument("--metrics", nargs="*", default=[settings["defaults"]["metric"]])
parser.add_argument(
    "--metric_evaluator", default="CumulativeInteractionMetricEvaluator"
)
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
settings["defaults"]["metric_evaluator"] = args.metric_evaluator

utils.eval_agent_search(args.agents,args.dataset_loaders,
        settings,agents_search,args.metrics, args.tasks)
