import shutil
import logging
import argparse
import os
from uuid import uuid4
import glob

logger = logging.getLogger(__name__)

COMPONENTS = (
    "cinder",
    "nova",
    "neutron",
    "glance",
    "keystone"
)


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", '-v', action='store_true', help='verbose mode')
    parser.add_argument("--debug", '-d', action='store_true', help='debug mode')
    parser.add_argument("--templates", '-t', help='set template directory', default="templates/")
    parser.add_argument("--out-dir", '-o', help='if set, copy the files in this directory', default=None)
    parser.add_argument("wrapper_url", help='Wrapper URL to use', nargs="*",
                        default=["http://127.0.0.1:8080/policy_checker"])
    args = parser.parse_args()
    logging_format = "%(levelname)s: %(message)s"
    if args.verbose:
        logging.basicConfig(level=logging.INFO, format=logging_format)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format=logging_format)
    return args


def update_templates(templates_dir, wrapper_url):
    tmp_dir = os.path.join("/tmp", str(uuid4()))
    wrapper_url = wrapper_url[0].strip('"').strip("'")
    os.mkdir(tmp_dir)
    for comp in COMPONENTS:
        input_file = os.path.join(templates_dir, comp + ".policy.json")
        output_file = os.path.join(tmp_dir, comp + ".policy.json")
        output_fd = open(output_file, "w")
        for line in open(input_file):
            output_fd.write(line.replace("{{wrapper}}", wrapper_url))
    return tmp_dir


def remove_tmp_files(tmp_dir):
    for _filename in glob.glob(os.path.join(tmp_dir, "*")):
        logger.debug("{} {}".format(_filename, os.path.isfile(_filename)))
        if os.path.isfile(_filename):
            logger.debug("Trying to delete {}".format(_filename))
            os.remove(_filename)
            logger.debug("Delete done")
    os.removedirs(tmp_dir)


def main(templates_dir, wrapper_url, out_dir=None):
    logger.info("Moving configuration files")
    tmp_dir = update_templates(templates_dir, wrapper_url)
    if out_dir:
        logger.info("Moving to {}".format(out_dir))
        try:
            os.mkdir(out_dir)
        except FileExistsError:
            logger.warning("Output directory exists, writing on it!")
        for comp in COMPONENTS:
            logger.info("Moving {}".format(comp))
            shutil.copy(os.path.join(tmp_dir, comp + ".policy.json"),
                        os.path.join(out_dir, comp + ".policy.json"))
    else:
        logger.info("Moving to /etc")
        for comp in COMPONENTS:
            logger.info("Moving {}".format(comp))
            shutil.copy(os.path.join(tmp_dir, comp + ".policy.json"),
                        os.path.join("etc", comp, "policy.json"))
    remove_tmp_files(tmp_dir)


if __name__ == "__main__":
    args = init()
    main(args.templates, args.wrapper_url, args.out_dir)
