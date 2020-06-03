from uuid import uuid4
import copy
import logging
import threading
import time
import json
import random
import requests

HOST_MANAGER = None
PORT_MANAGER = None
HOST_KEYSTONE = None
PORT_KEYSTONE = None

LOCK = threading.Lock()
LOGGER = logging.getLogger("moonclient.core.authz")


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
        _data = {'rule': current_rule,
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
            # with LOCK:
            res = requests.get(url)
            current_request['end'] = time.time()
            current_request['delta'] = current_request["end"] - current_request["start"]
        else:
            with LOCK:
                current_request['start'] = time.time()
                if data:
                    data, _ = _construct_payload(data['credentials'], data['rule'], True,
                                                 data['target'])
                    res = requests.post(url, json=data,
                                        headers={'content-type': "application/x-www-form-urlencode"}
                                        )
                else:
                    res = requests.get(url)
                current_request['end'] = time.time()
                current_request['delta'] = current_request["end"] - current_request["start"]
    except requests.exceptions.ConnectionError:
        LOGGER.warning("Unable to connect to server")
        return {}
    if not stress_test:
        try:
            j = res.json()
            if res.status_code == 200:
                LOGGER.warning("\033[1m{}\033[m \033[32mGrant\033[m".format(url))
            elif res.status_code == 401:
                LOGGER.warning("\033[1m{}\033[m \033[31mDeny\033[m".format(url))
            else:
                LOGGER.error("\033[1m{}\033[m {} {}".format(url, res.status_code, res.text))
        except Exception as e:
            if res.text == "True":
                LOGGER.warning("\033[1m{}\033[m \033[32mGrant\033[m".format(url))
            elif res.text == "False":
                LOGGER.warning("\033[1m{}\033[m \033[31mDeny\033[m".format(url))
            else:
                LOGGER.error("\033[1m{}\033[m {} {}".format(url, res.status_code, res.text))
                LOGGER.exception(e)
                LOGGER.error(res.text)
        else:
            if j.get("result"):
                # logger.warning("{} \033[32m{}\033[m".format(url, j.get("result")))
                LOGGER.debug("{}".format(j.get("error", "")))
                current_request['result'] = "Grant"
            else:
                # logger.warning("{} \033[31m{}\033[m".format(url, "Deny"))
                LOGGER.debug("{}".format(j))
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


def send_requests(scenario, authz_host, authz_port, keystone_project_id, request_second=1,
                  limit=500,
                  dry_run=None, stress_test=False, destination="wrapper"):
    backgrounds = []
    time_data = list()
    start_timing = time.time()
    request_cpt = 0
    subjects = tuple(scenario.subjects.keys())
    objects = tuple(scenario.objects.keys())
    actions = tuple(scenario.actions.keys())
    while request_cpt < limit:
        rule = (random.choice(subjects), random.choice(objects), random.choice(actions))
        if destination.lower() == "wrapper":
            url = "http://{}:{}/authz/oslo".format(authz_host, authz_port)
            data = {
                'target': {
                    "user_id": random.choice(subjects),
                    "target": {
                        "name": random.choice(objects)
                    },
                    "project_id": keystone_project_id
                },
                'credentials': None,
                'rule': random.choice(actions)
            }
        else:
            url = "http://{}:{}/authz/{}/{}".format(authz_host, authz_port, keystone_project_id,
                                                    "/".join(rule))
            data = None
        if dry_run:
            LOGGER.info(url)
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
                if time.time() - start_timing < 1:
                    while True:
                        if time.time() - start_timing > 1:
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
