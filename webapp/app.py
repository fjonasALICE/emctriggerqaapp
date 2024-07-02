#! /usr/bin/env python3

import os

from flask import Flask, render_template

app = Flask("offlineTriggerQA")

repo = os.environ["DATAPATH"]

def find_periods() -> list:
    if os.path.exists(repo):
        return sorted([x for x in os.listdir(repo) if "LHC" in x])
    return []

def find_runs(perioddir: str):
    return sorted([int(x) for x in os.listdir(perioddir) if x.isdigit()])

def find_plots_for_run(rundir: str) -> list:
    return [x for x in os.listdir(rundir) if x.endswith("png")]

def find_trending_plots(perioddir: str):
    return [x for x in os.listdir(perioddir) if x.endswith(".png")]

def categorize_trending_plots(trendingplots: list) -> dict:
    categorized = {"Absolute": {}, "Deviaton": {}}
    for plot in trendingplots:
        plotbase = os.path.basename(plot)
        key = ""
        if "Rejection" in plotbase:
            key = "Absolute"
        elif "RejDeviation" in plotbase:
            key = "Deviaton"
        trigger = ""
        if "FullJetTrigger" in plotbase:
            trigger = "jet"
        elif "PhotonTrigger" in plotbase:
            trigger = "photon"
        elif "AnyEMCTrigger" in plotbase:
            trigger = "any"
        if not len(key) and not len(trigger):
            continue
        categorized[key][trigger] = plot
    return categorized

def read_changelog() -> dict:
    changes = {}
    changelogfile = os.path.join(repo, "changelog.txt")
    currentchanges = []
    currenttimestamp = None
    if os.path.exists(changelogfile):
        with open(changelogfile, "r") as changelogreader:
            for line in changelogreader:
                line = line.rstrip("\n")
                print(f"Decoding {line}")
                if line.startswith("20"):
                    if len(currentchanges):
                        changes[currenttimestamp] = currentchanges
                    currentchanges = []
                    currenttimestamp = line.rstrip(":")
                elif "====" in line or not len(line):
                    continue
                else:
                    line = line[line.find("LHC"):]
                    tokens = line.split(",")
                    period = tokens[0]
                    runstring = tokens[1]
                    runnumber = int(runstring.replace("run", "").lstrip().rstrip())
                    currentchanges.append({"period": period, "run": runnumber})
    if len(currentchanges):
        changes[currenttimestamp] = currentchanges
    return changes

@app.route("/<period>", methods=["GET"])
def display_period(period: str):
    trendingplots = [f"{period}/{x}" for x in find_trending_plots(os.path.join(repo, period))]
    categorized_trendings = categorize_trending_plots(trendingplots)
    runs = find_runs(os.path.join(repo, period))
    plots = {}
    for run in runs:
        runplots = find_plots_for_run(os.path.join(repo, period, f"{run}"))
        categorized = {}
        for plot in runplots:
            plotname = f"{period}/{run}/{plot}"
            if "PhotonTriggerQA" in plot:
                categorized["photon"] = plotname
            else:
                categorized["jet"] = plotname
        plots[run] = categorized
    return render_template('period.html',
                           title=f"QA plots for period {period}",
                           runs = runs,
                           plots = plots,
                           trendings = categorized_trendings)

@app.route("/changelog")
def display_changelog():
    changes = read_changelog()
    return render_template('changelog.html',
                           title="Changelog",
                           timestamps = sorted(changes.keys()),
                           changes = changes)

@app.route("/")
def mainpage():
    return render_template('start.html',
                           title="Welcome to the ALICE Offline Trigger monitoring",
                           listitems = find_periods())

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')