import json
import logging
import requests
import argparse

URLS = {
    "keystone": "https://api.github.com/repos/openstack/keystone/contents/api-ref/source/v3",
    "nova": "https://api.github.com/repos/openstack/nova/contents/api-ref/source",
    "neutron": "https://api.github.com/repos/openstack/neutron-lib/contents/api-ref/source/v2",
    "glance": "https://api.github.com/repos/openstack/glance/contents/api-ref/source/v2",
    "swift": "https://api.github.com/repos/openstack/swift/contents/api-ref/source",
    "cinder": "https://api.github.com/repos/openstack/cinder/contents/api-ref/source/v3",

}

logger = None

USER = ""
PASS = ""


def init():
    global logger, USER, PASS
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action='store_true', help="verbose mode")
    parser.add_argument("--debug", "-d", action='store_true', help="debug mode")
    parser.add_argument("--format", "-f", help="Output format (txt, json)", default="json")
    parser.add_argument("--output", "-o", help="Output filename")
    parser.add_argument("--credentials", "-c", help="Github credential filename (inside format user:pass)")
    args = parser.parse_args()

    FORMAT = '%(levelname)s %(message)s'

    if args.verbose:
        logging.basicConfig(
            format=FORMAT,
            level=logging.INFO)
    elif args.debug:
        logging.basicConfig(
            format=FORMAT,
            level=logging.DEBUG)
    else:
        logging.basicConfig(
            format=FORMAT,
            level=logging.WARNING)

    if args.credentials:
        cred = open(args.credentials).read()
        USER = cred.split(":")[0]
        PASS = cred.split(":")[1]

    logger = logging.getLogger(__name__)

    return args


def get_api_item(url):
    if USER:
        r = requests.get(url, auth=(USER, PASS))
    else:
        r = requests.get(url)
    items = []
    for line in r.text.splitlines():
        if ".. rest_method::" in line:
            items.append(line.replace(".. rest_method::", "").strip())
    logger.debug("\n\t".join(items))
    return items


def get_content(key, args):
    logger.info("Analysing {}".format(key))
    if USER:
        r = requests.get(URLS[key], auth=(USER, PASS))
    else:
        r = requests.get(URLS[key])
    data = r.json()
    results = {}
    for item in data:
        try:
            logger.debug("{} {}".format(item['name'], item['download_url']))
            if item['type'] == "file" and ".inc" in item['name']:
                results[item['name'].replace(".inc", "")] = get_api_item(item['download_url'])
        except TypeError:
            logger.error("Error with {}".format(item))
        except requests.exceptions.MissingSchema:
            logger.error("MissingSchema error {}".format(item))
    return results


def to_str(results):
    output = ""
    for key in results:
        output += "{}\n".format(key)
        for item in results[key]:
            output += "\t{}\n".format(item)
            for value in results[key][item]:
                output += "\t\t{}\n".format(value)
    return output


def save(results, args):
    if args.output:
        if args.format == 'json':
            json.dump(results, open(args.output, "w"), indent=4)
        elif args.format == 'txt':
            open(args.output, "w").write(to_str(results))
    else:
        if args.format == 'json':
            print(json.dumps(results, indent=4))
        elif args.format in ('txt', 'text'):
            print(to_str(results))


def main():
    args = init()
    results = {}
    for key in URLS:
        results[key] = get_content(key, args)
    save(results, args)

if __name__ == "__main__":
    main()