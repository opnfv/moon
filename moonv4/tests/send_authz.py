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
import random
import plotly
from plotly.graph_objs import Scatter, Layout
import plotly.figure_factory as ff
from uuid import uuid4
from utils.pdp import check_pdp


logger = None
HOST = None
PORT = None
HOST_AUTHZ = None
PORT_AUTHZ = None
HOST_KEYSTONE = None
PORT_KEYSTONE = None

lock = threading.Lock()


def init():
    global logger, HOST, PORT, HOST_AUTHZ, PORT_AUTHZ, HOST_KEYSTONE, PORT_KEYSTONE
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='scenario filename', nargs=1)
    parser.add_argument("--verbose", "-v", action='store_true', help="verbose mode")
    parser.add_argument("--debug", action='store_true', help="debug mode")
    parser.add_argument("--dry-run", "-n", action='store_true', help="Dry run", dest="dry_run")
    parser.add_argument("--host",
                        help="Set the name of the host to test (default: 172.18.0.11).",
                        default="127.0.0.1")
    parser.add_argument("--port", "-p",
                        help="Set the port of the host to test (default: 8082).",
                        default="8082")
    parser.add_argument("--host-authz",
                        help="Set the name of the host to test authorization (default: 172.18.0.11).",
                        default="127.0.0.1",
                        dest="host_authz")
    parser.add_argument("--port-authz",
                        help="Set the port of the host to test authorization (default: 8081).",
                        default="8081",
                        dest="port_authz")
    parser.add_argument("--host-keystone",
                        help="Set the name of the Keystone host (default: 172.18.0.11).",
                        default="127.0.0.1")
    parser.add_argument("--port-keystone",
                        help="Set the port of the Keystone host (default: 5000).",
                        default="5000")
    parser.add_argument("--stress-test", "-s", action='store_true', dest='stress_test',
                        help="Execute stressing tests (warning delta measures will be false, implies -t)")
    parser.add_argument("--write", "-w", help="Write test data to a JSON file", default="/tmp/data.json")
    parser.add_argument("--pdp", help="Test on pdp PDP")
    parser.add_argument("--request-per-second", help="Number of requests per seconds",
                        type=int, dest="request_second", default=-1)
    parser.add_argument("--limit", help="Limit request to LIMIT", type=int, default=500)
    args = parser.parse_args()

    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    if args.debug:
        logging.basicConfig(
            format=FORMAT,
            level=logging.DEBUG)
    elif args.verbose:
        logging.basicConfig(
            format=FORMAT,
            level=logging.INFO)
    else:
        logging.basicConfig(
            format=FORMAT,
            level=logging.WARNING)

    logger = logging.getLogger(__name__)

    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = True

    if args.stress_test:
        args.testonly = True

    if args.filename:
        logger.info("Loading: {}".format(args.filename[0]))

    HOST = args.host
    PORT = args.port
    HOST_AUTHZ = args.host_authz
    PORT_AUTHZ = args.port_authz
    HOST_KEYSTONE = args.host_keystone
    PORT_KEYSTONE = args.port_keystone
    return args


def get_scenario(args):
    m = SourceFileLoader("scenario", args.filename[0])
    return m.load_module()


def get_keystone_id(pdp_name):
    keystone_project_id = None
    # logger.error("get_keystone_id url={}".format("http://{}:{}".format(HOST_KEYSTONE, PORT_KEYSTONE)))
    for pdp_key, pdp_value in check_pdp(moon_url="http://{}:{}".format(HOST, PORT))["pdps"].items():
        logger.debug(pdp_value)
        if pdp_name:
            if pdp_name != pdp_value["name"]:
                continue
        if pdp_value['security_pipeline'] and pdp_value["keystone_project_id"]:
            logger.debug("Found pdp with keystone_project_id={}".format(pdp_value["keystone_project_id"]))
            keystone_project_id = pdp_value["keystone_project_id"]

    if not keystone_project_id:
        logger.error("Cannot find PDP with keystone project ID")
        sys.exit(1)
    return keystone_project_id


def _send(url, stress_test=False):
    current_request = dict()
    current_request['url'] = url
    try:
        if stress_test:
            current_request['start'] = time.time()
            # with lock:
            res = requests.get(url)
            current_request['end'] = time.time()
            current_request['delta'] = current_request["end"] - current_request["start"]
        else:
            with lock:
                current_request['start'] = time.time()
                res = requests.get(url)
                current_request['end'] = time.time()
                current_request['delta'] = current_request["end"] - current_request["start"]
    except requests.exceptions.ConnectionError:
        logger.warning("Unable to connect to server")
        return {}
    if res and not stress_test:
        logger.debug(res.status_code)
        logger.debug(res.text)
        if res.status_code == 200:
            # logger.warning("error code 200 for {}".format(self.url))
            logger.info("\033[1m{}\033[m {}".format(url, res.status_code))
        try:
            j = res.json()
        except Exception as e:
            logger.debug(e)
            logger.error(res.text)
        else:
            if j.get("authz"):
                logger.warning("{} \033[32m{}\033[m".format(url, j.get("authz")))
                logger.debug("{}".format(j.get("error", "")))
                current_request['result'] = "Grant"
            else:
                logger.warning("{} \033[31m{}\033[m".format(url, j.get("authz")))
                logger.debug("{}".format(j.get("error", "")))
                current_request['result'] = "Deny"
    return current_request


class AsyncGet(threading.Thread):

    def __init__(self, url, semaphore=None, *args, **kwargs):
        threading.Thread.__init__(self)
        self.url = url
        self.kwargs = kwargs
        self.sema = semaphore
        self.result = dict()
        self.uuid = uuid4().hex
        self.index = kwargs.get("index", 0)

    def run(self):
        self.result = _send(self.url, self.kwargs.get("stress_test", False))
        self.result['index'] = self.index


def send_requests(scenario, keystone_project_id, request_second=1, limit=500,
                  dry_run=None, stress_test=False):
    # sema = threading.BoundedSemaphore(value=request_second)
    backgrounds = []
    time_data = list()
    start_timing = time.time()
    request_cpt = 0
    indexes = []
    # rules = itertools.product(scenario.subjects.keys(), scenario.objects.keys(), scenario.actions.keys())
    SUBJECTS = tuple(scenario.subjects.keys())
    OBJECTS = tuple(scenario.objects.keys())
    ACTIONS = tuple(scenario.actions.keys())
    # for rule in rules:
    while request_cpt < limit:
        rule = (random.choice(SUBJECTS), random.choice(OBJECTS), random.choice(ACTIONS))
        url = "http://{}:{}/authz/{}/{}".format(HOST_AUTHZ, PORT_AUTHZ, keystone_project_id, "/".join(rule))
        indexes.append(url)
        if dry_run:
            logger.info(url)
            continue
        request_cpt += 1
        if stress_test:
            time_data.append(copy.deepcopy(_send(url, stress_test=stress_test)))
        else:
            background = AsyncGet(url, stress_test=stress_test, index=request_cpt)
            backgrounds.append(background)
            background.start()
        # if limit and limit < request_cpt:
        #     break
        if request_second > 0:
            if request_cpt % request_second == 0:
                if time.time()-start_timing < 1:
                    while True:
                        if time.time()-start_timing > 1:
                            break
                start_timing = time.time()
    if not stress_test:
        for background in backgrounds:
            background.join()
            if background.result:
                time_data.append(copy.deepcopy(background.result))
    return time_data


def save_data(filename, time_data):
    json.dump(time_data, open(filename, "w"))


def get_delta(time_data):
    time_delta = list()
    time_delta_sum1 = 0
    for item in time_data:
        time_delta.append(item['delta'])
        time_delta_sum1 += item['delta']
    time_delta_average1 = time_delta_sum1 / len(time_data)
    return time_delta, time_delta_average1


def main():
    args = init()
    scenario = get_scenario(args)
    keystone_project_id = get_keystone_id(args.pdp)
    time_data = send_requests(
        scenario,
        keystone_project_id,
        request_second=args.request_second,
        limit=args.limit,
        dry_run=args.dry_run,
        stress_test=args.stress_test
    )
    if not args.dry_run:
        save_data(args.write, time_data)


if __name__ == "__main__":
    main()
