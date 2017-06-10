import sys
import argparse
import logging
import copy
import threading
from importlib.machinery import SourceFileLoader
import itertools
import requests
import time
import json
import plotly
from plotly.graph_objs import Scatter, Layout
import plotly.figure_factory as ff
from uuid import uuid4
from utils.pdp import check_pdp


logger = None
HOST = None
PORT = None

lock = threading.Lock()


def init():
    global logger, HOST, PORT
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='scenario filename', nargs=1)
    parser.add_argument("--verbose", "-v", action='store_true', help="verbose mode")
    parser.add_argument("--host",
                        help="Set the name of the host to test (default: 172.18.0.11).",
                        default="172.18.0.11")
    parser.add_argument("--port", "-p",
                        help="Set the port of the host to test (default: 38001).",
                        default="38001")
    parser.add_argument("--test-only", "-t", action='store_true', dest='testonly', help="Do not generate graphs")
    parser.add_argument("--write", "-w", help="Write test data to a JSON file", default="/tmp/data.json")
    parser.add_argument("--input", "-i", help="Get data from a JSON input file")
    parser.add_argument("--legend", "-l", help="Set the legend (default: 'rbac,rbac+session')",
                        default='rbac,rbac+session')
    parser.add_argument("--distgraph", "-d",
                        help="Show a distribution graph instead of a linear graph",
                        action='store_true')
    parser.add_argument("--request-per-second", help="Number of requests per seconds",
                        type=int, dest="request_second", default=1)
    parser.add_argument("--limit", help="Limit request to LIMIT", type=int)
    parser.add_argument("--write-image", help="Write the graph to file IMAGE", dest="write_image")
    parser.add_argument("--write-html", help="Write the graph to HTML file HTML", dest="write_html", default="data.html")
    args = parser.parse_args()

    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    logging.basicConfig(
        format=FORMAT,
        level=logging.INFO)

    logger = logging.getLogger(__name__)

    if args.filename:
        logger.info("Loading: {}".format(args.filename[0]))

    HOST = args.host
    PORT = args.port
    return args


def get_scenario(args):
    m = SourceFileLoader("scenario", args.filename[0])
    return m.load_module()


def get_keystone_id():
    keystone_project_id = None
    for pdp_key, pdp_value in check_pdp(moon_url="http://{}:{}".format(HOST, PORT))["pdps"].items():
        print(pdp_value)
        if pdp_value['security_pipeline'] and pdp_value["keystone_project_id"]:
            print("Found pdp with keystone_project_id={}".format(pdp_value["keystone_project_id"]))
            keystone_project_id = pdp_value["keystone_project_id"]

    if not keystone_project_id:
        logger.error("Cannot find PDP with keystone project ID")
        sys.exit(1)
    return keystone_project_id


class AsyncGet(threading.Thread):
    def __init__(self, url, semaphore=None, *args, **kwargs):
        threading.Thread.__init__(self)
        self.url = url
        self.kwargs = kwargs
        self.sema = semaphore
        self.result = dict()
        self.uuid = uuid4().hex

    def run(self):

        # self.sema.acquire()
        current_request = dict()
        current_request['url'] = self.url
        try:
            with lock:
                current_request['start'] = time.time()
                r = requests.get(self.url, **self.kwargs)
                current_request['end'] = time.time()
                current_request['delta'] = current_request["end"] - current_request["start"]
        except requests.exceptions.ConnectionError:
            logger.warning("Unable to connect to server")
            return {}
        if r:
            logger.debug(r.status_code)
            logger.debug(r.text)
            if r.status_code == 200:
                logger.warning("error code 200 for {}".format(self.url))
                logger.info("\033[1m{}\033[m {}".format(self.url, r.status_code))
            try:
                j = r.json()
            except Exception as e:
                logger.error(r.text)
            else:
                if j.get("authz"):
                    logger.info("\t\033[32m{}\033[m {}".format(j.get("authz"), j.get("error", "")))
                else:
                    logger.info("\t\033[31m{}\033[m {}".format(j.get("authz"), j.get("error", "")))
        self.result = current_request
        # self.sema.release()


def send_requests(scenario, keystone_project_id, request_second=1, limit=None):
    # sema = threading.BoundedSemaphore(value=request_second)
    backgrounds = []
    time_data = dict()
    start_timing = time.time()
    request_cpt = 0
    rules = itertools.product(scenario.subjects.keys(), scenario.objects.keys(), scenario.actions.keys())
    for rule in rules:
        url = "http://{}:{}/authz/{}/{}".format(HOST, PORT, keystone_project_id, "/".join(rule))
        request_cpt += 1
        background = AsyncGet(url)
        backgrounds.append(background)
        background.start()
        if limit and limit < request_cpt:
            break
        if request_cpt % request_second == 0:
            if time.time()-start_timing < 1:
                while True:
                    if time.time()-start_timing > 1:
                        break
            start_timing = time.time()
    for background in backgrounds:
        background.join()
        if background.result:
            time_data[background.url] = copy.deepcopy(background.result)
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


def write_graph(time_data, legend=None, input=None, image_file=None, html_file=None):
    logger.info("Writing graph")
    legends = legend.split(",")
    result_data = []
    time_delta, time_delta_average1 = get_delta(time_data)
    time_delta_average2 = None
    if input:
        for _input in input.split(","):
            current_legend = legends.pop(0)
            time_data2 = json.load(open(_input))
            time_delta2, time_delta_average2 = get_delta(time_data2)
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
    current_legend = legends.pop(0)
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

    if image_file:
        plotly.offline.plot(
            {
                "data": result_data,
                "layout": Layout(
                    title="Request times delta",
                    xaxis=dict(title='Requests'),
                    yaxis=dict(title='Request duration'),
                )
            },
            filename=html_file,
            image="svg",
            image_filename=image_file,
            image_height=1000,
            image_width=1200
        )
    else:
        plotly.offline.plot(
            {
                "data": result_data,
                "layout": Layout(
                    title="Request times delta",
                    xaxis=dict(title='Requests'),
                    yaxis=dict(title='Request duration'),
                )
            },
            filename=html_file,
        )
    if time_delta_average2:
        logger.info("Average: {} and {}".format(time_delta_average1, time_delta_average2))
        return 1-time_delta_average2/time_delta_average1
    return 0


def write_distgraph(time_data, legend=None, input=None, image_file=None, html_file=None):

    logger.info("Writing graph")
    legends = legend.split(",")
    result_data = []

    time_delta_average2 = None

    if input:
        for _input in input.split(","):
            logger.info("Analysing input {}".format(_input))
            time_data2 = json.load(open(_input))
            time_delta2, time_delta_average2 = get_delta(time_data2)
            result_data.append(time_delta2)

    time_delta, time_delta_average1 = get_delta(time_data)
    result_data.append(time_delta)

    # Create distplot with custom bin_size
    if len(legends) < len(result_data):
        for _cpt in range(len(result_data)-len(legends)):
            legends.append("NC")
    fig = ff.create_distplot(result_data, legends, bin_size=.2)

    # Plot!
    plotly.offline.plot(
        fig,
        image="svg",
        image_filename=image_file,
        image_height=1000,
        image_width=1200,
        filename=html_file
    )
    if time_delta_average2:
        logger.info("Average: {} and {}".format(time_delta_average1, time_delta_average2))
        return 1-time_delta_average2/time_delta_average1
    return 0


def main():
    args = init()
    scenario = get_scenario(args)
    keystone_project_id = get_keystone_id()
    time_data = send_requests(scenario, keystone_project_id, request_second=args.request_second, limit=args.limit)
    save_data(args.write, time_data)
    if not args.testonly:
        if args.distgraph:
            overhead = write_distgraph(time_data, legend=args.legend, input=args.input, image_file=args.write_image,
                                       html_file=args.write_html)
        else:
            overhead = write_graph(time_data, legend=args.legend, input=args.input, image_file=args.write_image,
                                   html_file=args.write_html)
        logger.info("Overhead: {:.2%}".format(overhead))


if __name__ == "__main__":
    main()
