import logging
import argparse


logger = None


def parse():
    global logger
    logger = logging.getLogger("python_moonclient.utils.parse")
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = True

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='scenario filename', nargs="*")
    parser.add_argument("--verbose", "-v", action='store_true',
                        help="verbose mode")
    parser.add_argument("--debug", "-d", action='store_true',
                        help="debug mode")
    parser.add_argument("--dry-run", "-n", action='store_true',
                        help="Dry run", dest="dry_run")
    parser.add_argument("--destination",
                        help="Set the type of output needed "
                             "(default: wrapper, other possible type: "
                             "interface).",
                        default="wrapper")
    parser.add_argument("--consul-host",
                        help="Set the name of the consul server"
                             "(default: 127.0.0.1).",
                        default="127.0.0.1")
    parser.add_argument("--consul-port",
                        help="Set the port of the consult server"
                             "(default: 30005).",
                        default="30005")
    parser.add_argument("--authz-host",
                        help="Set the name of the authz server to test"
                             "(default: 127.0.0.1).",
                        default="127.0.0.1")
    parser.add_argument("--authz-port",
                        help="Set the port of the authz server to test"
                             "(default: 31002).",
                        default="31002")
    parser.add_argument("--keystone-pid", "--keystone-project-id",
                        help="Set the Keystone project ID"
                             "(default: None).",
                        default=None)
    parser.add_argument("--stress-test", "-s", action='store_true',
                        dest='stress_test',
                        help="Execute stressing tests (warning delta measures "
                             "will be false, implies -t)")
    parser.add_argument("--write", "-w", help="Write test data to a JSON file",
                        default="/tmp/data.json")
    parser.add_argument("--pdp", help="Test on pdp PDP")
    parser.add_argument("--request-per-second",
                        help="Number of requests per seconds",
                        type=int, dest="request_second", default=-1)
    parser.add_argument("--limit", help="Limit request to LIMIT", type=int,
                        default=500)

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

    if args.stress_test:
        args.testonly = True

    if args.filename:
        logger.info("Loading: {}".format(args.filename[0]))

    return args
