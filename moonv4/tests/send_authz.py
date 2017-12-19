import sys
import copy
import logging
import threading
from importlib.machinery import SourceFileLoader
import requests
import time
import json
import random
from uuid import uuid4
from utils.pdp import check_pdp
from utils.parse import parse
import utils.config


logger = None
HOST_MANAGER = None
PORT_MANAGER = None
HOST_AUTHZ = None
PORT_AUTHZ = None
HOST_KEYSTONE = None
PORT_KEYSTONE = None

lock = threading.Lock()
logger = logging.getLogger(__name__)


def get_scenario(args):
    m = SourceFileLoader("scenario", args.filename[0])
    return m.load_module()


def get_keystone_id(pdp_name):
    global HOST_MANAGER, PORT_MANAGER
    keystone_project_id = None
    for pdp_key, pdp_value in check_pdp(moon_url="http://{}:{}".format(HOST_MANAGER, PORT_MANAGER))["pdps"].items():
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


def _construct_payload(creds, current_rule, enforcer, target):
    # Convert instances of object() in target temporarily to
    # empty dict to avoid circular reference detection
    # errors in jsonutils.dumps().
    temp_target = copy.deepcopy(target)
    for key in target.keys():
        element = target.get(key)
        if type(element) is object:
            temp_target[key] = {}
    _data = _json = None
    if enforcer:
        _data = {'rule': json.dumps(current_rule),
                 'target': json.dumps(temp_target),
                 'credentials': json.dumps(creds)}
    else:
        _json = {'rule': current_rule,
                 'target': temp_target,
                 'credentials': creds}
    return _data, _json


def _send(url, data=None, stress_test=False):
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
                if data:
                    data, _ = _construct_payload(data['credentials'], data['rule'], True, data['target'])
                    res = requests.post(url, json=data,
                                        headers={'content-type': "application/x-www-form-urlencode"}
                                        )
                else:
                    res = requests.get(url)
                current_request['end'] = time.time()
                current_request['delta'] = current_request["end"] - current_request["start"]
    except requests.exceptions.ConnectionError:
        logger.warning("Unable to connect to server")
        return {}
    if not stress_test:
        try:
            j = res.json()
            if res.status_code == 200:
                logger.warning("\033[1m{}\033[m \033[32mGrant\033[m".format(url))
            elif res.status_code == 401:
                logger.warning("\033[1m{}\033[m \033[31mDeny\033[m".format(url))
            else:
                logger.error("\033[1m{}\033[m {} {}".format(url, res.status_code, res.text))
        except Exception as e:
            if res.text == "True":
                logger.warning("\033[1m{}\033[m \033[32mGrant\033[m".format(url))
            elif res.text == "False":
                logger.warning("\033[1m{}\033[m \033[31mDeny\033[m".format(url))
            else:
                logger.error("\033[1m{}\033[m {} {}".format(url, res.status_code, res.text))
                logger.exception(e)
                logger.error(res.text)
        else:
            if j.get("result"):
                # logger.warning("{} \033[32m{}\033[m".format(url, j.get("result")))
                logger.debug("{}".format(j.get("error", "")))
                current_request['result'] = "Grant"
            else:
                # logger.warning("{} \033[31m{}\033[m".format(url, "Deny"))
                logger.debug("{}".format(j))
                current_request['result'] = "Deny"
    return current_request


class AsyncGet(threading.Thread):

    def __init__(self, url, semaphore=None, **kwargs):
        threading.Thread.__init__(self)
        self.url = url
        self.kwargs = kwargs
        self.sema = semaphore
        self.result = dict()
        self.uuid = uuid4().hex
        self.index = kwargs.get("index", 0)

    def run(self):
        self.result = _send(self.url,
                            data=self.kwargs.get("data"),
                            stress_test=self.kwargs.get("stress_test", False))
        self.result['index'] = self.index


def send_requests(scenario, keystone_project_id, request_second=1, limit=500,
                  dry_run=None, stress_test=False, destination="wrapper"):
    global HOST_AUTHZ, PORT_AUTHZ
    backgrounds = []
    time_data = list()
    start_timing = time.time()
    request_cpt = 0
    SUBJECTS = tuple(scenario.subjects.keys())
    OBJECTS = tuple(scenario.objects.keys())
    ACTIONS = tuple(scenario.actions.keys())
    while request_cpt < limit:
        rule = (random.choice(SUBJECTS), random.choice(OBJECTS), random.choice(ACTIONS))
        if destination.lower() == "wrapper":
            url = "http://{}:{}/authz".format(HOST_AUTHZ, PORT_AUTHZ)
            data = {
                'target': {
                    "user_id": random.choice(SUBJECTS),
                    "target": {
                        "name": random.choice(OBJECTS)
                    },
                    "project_id": keystone_project_id
                },
                'credentials': None,
                'rule': random.choice(ACTIONS)
            }
        else:
            url = "http://{}:{}/authz/{}/{}".format(HOST_AUTHZ, PORT_AUTHZ, keystone_project_id, "/".join(rule))
            data = None
        if dry_run:
            logger.info(url)
            continue
        request_cpt += 1
        if stress_test:
            time_data.append(copy.deepcopy(_send(url, stress_test=stress_test)))
        else:
            background = AsyncGet(url, stress_test=stress_test, data=data,
                                  index=request_cpt)
            backgrounds.append(background)
            background.start()
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
    global HOST_MANAGER, PORT_MANAGER, HOST_AUTHZ, PORT_AUTHZ

    args = parse()
    consul_host = args.consul_host
    consul_port = args.consul_port
    conf_data = utils.config.get_config_data(consul_host, consul_port)

    HOST_MANAGER = conf_data['manager_host']
    PORT_MANAGER = conf_data['manager_port']
    HOST_AUTHZ = args.authz_host
    PORT_AUTHZ = args.authz_port
    # HOST_KEYSTONE = conf_data['keystone_host']
    # PORT_KEYSTONE = conf_data['manager_host']

    scenario = get_scenario(args)
    keystone_project_id = get_keystone_id(args.pdp)
    time_data = send_requests(
        scenario,
        keystone_project_id,
        request_second=args.request_second,
        limit=args.limit,
        dry_run=args.dry_run,
        stress_test=args.stress_test,
        destination=args.destination
    )
    if not args.dry_run:
        save_data(args.write, time_data)


if __name__ == "__main__":
    main()
