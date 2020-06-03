import requests
from oslo_config import cfg
from oslo_log import log as logging
from python_moonutilities import exceptions

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


def login(user=None, password=None, domain=None, project=None, url=None):
    print("""Configuration:
    user: {user}
    domain: {domain}
    project: {project}
    url: {url}""".format(
        user=CONF.keystone.user,
        domain=CONF.keystone.domain,
        project=CONF.keystone.project,
        url=CONF.keystone.url,
    ))
    if not user:
        user = CONF.keystone.user
    if not password:
        password = CONF.keystone.password
    if not domain:
        domain = CONF.keystone.domain
    if not project:
        project = CONF.keystone.project
    if not url:
        url = CONF.keystone.url
    headers = {
        "Content-Type": "application/json"
    }
    data_auth = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "id": domain
                        },
                        "name": user,
                        "password": password
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "id": domain
                    },
                    "name": project
                }
            }
        }
    }

    req = requests.post("{}/auth/tokens".format(url),
                        json=data_auth, headers=headers,
                        verify=False)

    if req.status_code not in (200, 201):
        LOG.error(req.text)
        raise exceptions.KeystoneError
    headers['X-Auth-Token'] = req.headers['X-Subject-Token']
    return headers

print(login()['X-Auth-Token'])
