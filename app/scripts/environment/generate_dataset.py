#!/usr/bin/python3
from os.path import dirname, realpath, sep, pardir
import os
os.chdir(dirname(realpath(__file__)) + sep + pardir + sep + pardir + sep)
from irec.connector import utils
import argparse

settings = utils.load_settings(dirname(realpath(__file__)))
parser = argparse.ArgumentParser()
parser.add_argument(
    "--dataset_loaders", nargs="*", default=[settings["defaults"]["dataset_loader"]]
)
args = parser.parse_args()

for dataset_name in args.dataset_loaders:
    utils.generate_base(dataset_name,settings)
