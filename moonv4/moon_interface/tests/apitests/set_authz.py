import sys
import argparse
import logging
from importlib.machinery import SourceFileLoader
import itertools
import requests
import time
import json
import plotly
from plotly.graph_objs import Scatter, Layout
import plotly.figure_factory as ff
import numpy as np
from utils.pdp import check_pdp


logger = None


def init():
    global logger
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='scenario filename', nargs=1)
    parser.add_argument("--verbose", "-v", action='store_true', help="verbose mode")
    parser.add_argument("--test-only", "-t", action='store_true', dest='testonly', help="Do not generate graphs")
    parser.add_argument("--write", "-w", help="Write test data to a JSON file", default="/tmp/data.json")
    parser.add_argument("--input", "-i", help="Get data from a JSON input file")
    parser.add_argument("--legend", "-l", help="Set the legend (default: 'rbac,rbac+session')", default='rbac,rbac+session')
    parser.add_argument("--distgraph", "-d",
                        help="Show a distribution graph instead of a linear graph",
                        action='store_true')
    args = parser.parse_args()

    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    logging.basicConfig(
        format=FORMAT,
        level=logging.INFO)

    logger = logging.getLogger(__name__)

    if args.filename:
        logger.info("Loading: {}".format(args.filename[0]))

    return args


def get_scenario(args):
    m = SourceFileLoader("scenario", args.filename[0])
    return m.load_module()


def get_keystone_id():
    keystone_project_id = None
    for pdp_key, pdp_value in check_pdp()["pdps"].items():
        if pdp_value['security_pipeline'] and pdp_value["keystone_project_id"]:
            print("Found pdp with keystone_project_id={}".format(pdp_value["keystone_project_id"]))
            keystone_project_id = pdp_value["keystone_project_id"]

    if not keystone_project_id:
        logger.error("Cannot find PDP with keystone project ID")
        sys.exit(1)
    return keystone_project_id


def send_requests(scenario, keystone_project_id):
    time_data = dict()
    rules = itertools.product(scenario.subjects.keys(), scenario.objects.keys(), scenario.actions.keys())
    for rule in rules:
        current_request = dict()
        url = "http://172.18.0.11:38001/authz/{}/{}".format(keystone_project_id, "/".join(rule))
        current_request['url'] = url
        current_request['start'] = time.time()
        req = requests.get(url)
        print("\033[1m{}\033[m {}".format(url, req.status_code))
        try:
            j = req.json()
        except Exception as e:
            print(req.text)
        else:
            if j.get("authz"):
                logger.info("\t\033[32m{}\033[m {}".format(j.get("authz"), j.get("error", "")))
            else:
                logger.info("\t\033[31m{}\033[m {}".format(j.get("authz"), j.get("error", "")))
        current_request['end'] = time.time()
        current_request['delta'] = current_request["end"]-current_request["start"]
        time_data[url] = current_request
    return time_data


def save_data(filename, time_data):
    json.dump(time_data, open(filename, "w"))


def get_delta(time_data):
    time_delta = list()
    time_delta_sum1 = 0
    for key in time_data:
        time_delta.append(time_data[key]['delta'])
        time_delta_sum1 += time_data[key]['delta']
    time_delta_average1 = time_delta_sum1 / len(time_data.keys())
    return time_delta, time_delta_average1


def write_graph(time_data, legend=None, input=None):
    logger.info("Writing graph")
    legends = legend.split(",")
    result_data = []
    time_delta, time_delta_average1 = get_delta(time_data)
    # time_delta = list()
    # time_delta_sum1 = 0
    # for key in time_data:
    #     time_delta.append(time_data[key]['delta'])
    #     time_delta_sum1 += time_data[key]['delta']
    # time_delta_average1 = time_delta_sum1 / len(time_data.keys())
    current_legend = legends.pop()
    data1 = Scatter(
        x=list(range(len(time_data.keys()))),
        y=time_delta,
        name=current_legend,
        line=dict(
            color='rgb(123, 118, 255)',
            shape='spline')
    )
    result_data.append(data1)
    data1_a = Scatter(
        x=list(range(len(time_data.keys()))),
        y=[time_delta_average1 for x in range(len(time_data.keys()))],
        name=current_legend + " average",
        line=dict(
            color='rgb(28, 20, 255)',
            shape='spline')
    )
    result_data.append(data1_a)
    time_delta_average2 = None
    if input:
        current_legend = legends.pop()
        time_data2 = json.load(open(input))
        time_delta2, time_delta_average2 = get_delta(time_data2)
        # time_delta2 = list()
        # time_delta_sum2 = 0
        # for key in time_data2:
        #     time_delta.append(time_data2[key]['delta'])
        #     time_delta_sum2 += time_data2[key]['delta']
        # time_delta_average2 = time_delta_sum2 / len(time_data2.keys())
        for key in time_data.keys():
            if key in time_data2:
                time_delta2.append(time_data2[key]['delta'])
            else:
                time_delta2.append(None)
        data2 = Scatter(
            x=list(range(len(time_data.keys()))),
            y=time_delta2,
            name=current_legend,
            line=dict(
                color='rgb(255, 192, 118)',
                shape='spline')
        )
        result_data.append(data2)
        data2_a = Scatter(
            x=list(range(len(time_data.keys()))),
            y=[time_delta_average2 for x in range(len(time_data.keys()))],
            name=current_legend + " average",
            line=dict(
                color='rgb(255, 152, 33)',
                shape='spline')
        )
        result_data.append(data2_a)

    plotly.offline.plot({
        "data": result_data,
        "layout": Layout(
            title="Request times delta",
            xaxis=dict(title='Requests'),
            yaxis=dict(title='Request duration'),
        )
    })
    if time_delta_average2:
        logger.info("Average: {} and {}".format(time_delta_average1, time_delta_average2))
        return 1-time_delta_average2/time_delta_average1
    return 0


def write_distgraph(time_data, legend=None, input=None):

    logger.info("Writing graph")
    legends = legend.split(",")[::-1]
    result_data = []
    time_delta, time_delta_average1 = get_delta(time_data)
    result_data.append(time_delta)

    time_delta_average2 = None

    if input:
        time_data2 = json.load(open(input))
        time_delta2, time_delta_average2 = get_delta(time_data2)
        result_data.append(time_delta2)

    # Create distplot with custom bin_size
    fig = ff.create_distplot(result_data, legends, bin_size=.2)

    # Plot!
    plotly.offline.plot(fig)
    if time_delta_average2:
        logger.info("Average: {} and {}".format(time_delta_average1, time_delta_average2))
        return 1-time_delta_average2/time_delta_average1
    return 0


def main():
    args = init()
    scenario = get_scenario(args)
    keystone_project_id = get_keystone_id()
    time_data = send_requests(scenario, keystone_project_id)
    save_data(args.write, time_data)
    if not args.testonly:
        if args.distgraph:
            overhead = write_distgraph(time_data, legend=args.legend, input=args.input)
        else:
            overhead = write_graph(time_data, legend=args.legend, input=args.input)
        logger.info("Overhead: {:.2%}".format(overhead))


if __name__ == "__main__":
    main()
