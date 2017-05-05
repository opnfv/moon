import sys
import argparse
import logging
from importlib.machinery import SourceFileLoader
import itertools
import requests
from utils.pdp import check_pdp

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='scenario filename', nargs=1)
parser.add_argument("--verbose", "-v", action='store_true', help="verbose mode")
args = parser.parse_args()

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO)

logger = logging.getLogger(__name__)

if args.filename:
    print("Loading: {}".format(args.filename[0]))

m = SourceFileLoader("scenario", args.filename[0])

scenario = m.load_module()

rules = itertools.product(scenario.subjects.keys(), scenario.objects.keys(), scenario.actions.keys())

keystone_project_id = None
for pdp_key, pdp_value in check_pdp()["pdps"].items():
    if pdp_value['security_pipeline'] and pdp_value["keystone_project_id"]:
        print("Found pdp with keystone_project_id={}".format(pdp_value["keystone_project_id"]))
        keystone_project_id = pdp_value["keystone_project_id"]

if not keystone_project_id:
    logger.error("Cannot find PDP with keystone project ID")
    sys.exit(1)

for rule in rules:
    url = "http://172.18.0.11:38001/authz/{}/{}".format(keystone_project_id, "/".join(rule))
    req = requests.get(url)
    print("\033[1m{}\033[m {}".format(url, req.status_code))
    j = req.json()
    # print(j)
    if j.get("authz"):
        print("\t\033[32m{}\033[m {}".format(j.get("authz"), j.get("error", "")))
    else:
        print("\t\033[31m{}\033[m {}".format(j.get("authz"), j.get("error", "")))

