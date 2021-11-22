#!/bin/python3

import os, sys, re
import argparse

import numpy as np
import pandas as pd

RUN_PATH = "/eos/cms/store/group/dpg_gem/comm_gem/TestBeams/Oct2021/runs/"
log_folder = "log"
run_folders = dict(
    compressed = "compressed",
    raw = "raw",
    digi = "standalone/digi",
    rechits = "standalone/rechits"
)
run_extensions = dict(
    compressed = "-0-0.raw.zst",
    raw = "-0-0.raw",
    digi = ".root",
    rechits = ".root"
)
log_files = os.listdir(f"{RUN_PATH}/{log_folder}")

STR_NEVENTS = "Total number of events in the run"

class Run:
    def from_name(run_name):
        run = Run(run_name)
        run.log_file = f"{RUN_PATH}/{log_folder}/{run_name}.log"
        run.files = dict()
        for folder_key in run_folders:
            run.files[folder_key] = f"{RUN_PATH}/{run_folders[folder_key]}/{run_name}{run_extensions[folder_key]}"
        return run

    def __init__(self, run_name):
        self.run_name = run_name

    @property
    def event_count(self):
        lines = self.log_lines
        for line in lines:
            match = re.match(f"{STR_NEVENTS}: (\d+)", line)
            if match: return int(match.group(1))
        return -1

    @property
    def log_lines(self):
        with open(self.log_file, "r") as log_file:
            return log_file.readlines()

    def get_file(self, file_type):
        return self.files[file_type]

    def has_format(self, file_type):
        return os.path.exists(self.get_file(file_type))


class RunCollection:
    def __init__(self):
        self.runs = list()
    
    def append(self, run):
        self.runs.append(run)

    def to_dataframe(self):
        keys = ["name"] + list(run_folders.keys()) + ["events"]
        d = { key: list() for key in keys }
        for run in self.runs:
            d["name"].append(run.run_name)
            for key in run_folders:
                d[key].append(run.has_format(key))
            d["events"].append(run.event_count)
        return pd.DataFrame.from_dict(d)
    
    def __repr__(self):
        df = self.to_dataframe()
        return df.to_string()

def list_runs():
    run_collection = RunCollection()
    for log_filename in log_files:
        run = Run.from_name(log_filename.replace(".log", ""))
        run_collection.append(run)
    print(run_collection)

def search_run(run_name):
    run_collection = RunCollection()
    for log_filename in log_files:
        if run_name in log_filename:
            run = Run.from_name(log_filename.replace(".log", ""))
            run_collection.append(run)
    print(run_collection)

def print_run(run_name):
    run_filename = f"{RUN_PATH}/{log_folder}/{run_name}.log"
    try:
        with open(run_filename, "r") as run_file:
            run_log = run_file.read()
            print(run_log)
    except FileNotFoundError:
        print("No file found with given name")

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, help="Explore command")

    parser_list = subparsers.add_parser("list", help="List all runs")
    parser_list.set_defaults(func=lambda args: list_runs())

    parser_search = subparsers.add_parser("search", help="Search for run")
    parser_search.add_argument("run", type=str, help="Part of run name")
    parser_search.set_defaults(func=lambda args: search_run(args.run))

    parser_log = subparsers.add_parser("log", help="Print run log")
    parser_log.add_argument("run", type=str, help="Full run name")
    parser_log.set_defaults(func=lambda args: print_run(args.run))

    args = parser.parse_args()
    args.func(args)

if __name__=='__main__': main()