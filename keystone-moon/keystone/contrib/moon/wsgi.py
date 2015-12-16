from keystone.server import wsgi
from oslo_log import log

LOG = log.getLogger(__name__)


def initialize_moon_application():
    return wsgi.initialize_application('moon_service')
