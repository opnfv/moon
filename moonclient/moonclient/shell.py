# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging
import sys
import json
import httplib
import os

from cliff.app import App
from cliff.commandmanager import CommandManager


def get_env_creds(admin_token=False):
    d = dict()
    if 'OS_SERVICE_ENDPOINT' in os.environ.keys() or 'OS_USERNAME' in os.environ.keys():
        if admin_token:
            d['endpoint'] = os.environ['OS_SERVICE_ENDPOINT']
            d['token'] = os.environ['OS_SERVICE_TOKEN']
        else:
            d['username'] = os.environ['OS_USERNAME']
            d['password'] = os.environ['OS_PASSWORD']
            d['auth_url'] = os.environ['OS_AUTH_URL']
            d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d


class MoonClient(App):

    log = logging.getLogger(__name__)
    x_subject_token = None
    host = "localhost"
    port = "35358"
    tenant = None
    _intraextension = None
    _tenant_id = None
    _tenant_name = None
    secureprotocol = False
    user_saving_file = ".moonclient"
    url_prefix = "/moon"
    post = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "id": "Default"
                        },
                        "name": "admin",
                        "password": "nomoresecrete"
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "id": "Default"
                    },
                    "name": "demo"
                }
            }
        }
    }

    def __init__(self):
        super(MoonClient, self).__init__(
            description='Moon Python Client',
            version='0.1',
            command_manager=CommandManager('moon.client'),
            )
        creds = get_env_creds()
        self.post["auth"]["identity"]["password"]["user"]["password"] = creds["password"]
        self.post["auth"]["identity"]["password"]["user"]["name"] = creds["username"]
        self.post["auth"]["scope"]["project"]["name"] = creds["tenant_name"]
        self.host = creds["auth_url"].replace("https://", "").replace("http://", "").split("/")[0].split(":")[0]
        self.port = creds["auth_url"].replace("https://", "").replace("http://", "").split("/")[0].split(":")[1]
        if "https" in creds["auth_url"]:
            self.secureprotocol = True
        else:
            self.secureprotocol = False
        self._tenant_name = creds["tenant_name"]
        self.parser.add_argument(
            '--username',
            metavar='<username-str>',
            help='Force OpenStack username',
            default=None
        )
        self.parser.add_argument(
            '--tenant',
            metavar='<tenantname-str>',
            help='Force OpenStack tenant',
            default=None
        )
        self.parser.add_argument(
            '--password',
            metavar='<password-str>',
            help='Force OpenStack password',
            default=None
        )
        self.parser.add_argument(
            '--authurl',
            metavar='<authurl-str>',
            help='Force OpenStack authentication URL',
            default=None
        )

    @property
    def tenant_id(self):
        if not self._tenant_id:
            self._tenant_id = self.get_url("/v3/projects?name={}".format(self._tenant_name),
                                           authtoken=True, port=5000)["projects"][0]["id"]
        return self._tenant_id

    @property
    def tenant_name(self):
        return self._tenant_name

    @property
    def intraextension(self):
        return open(os.path.join(os.getenv('HOME'), self.user_saving_file)).read().strip()

    @intraextension.setter
    def intraextension(self, value):
        self._intraextension = value
        open(os.path.join(os.getenv('HOME'), self.user_saving_file), "w").write(value)

    def get_tenant_uuid(self, tenant_name):
        return self.get_url("/v3/projects?name={}".format(tenant_name), authtoken=True, port=5000)["projects"][0]["id"]

    def get_url(self, url, post_data=None, delete_data=None, method="GET", authtoken=None, port=None):
        if post_data:
            method = "POST"
        if delete_data:
            method = "DELETE"
        self.log.debug("\033[32m{} {}\033[m".format(method, url))
        # TODO: we must manage authentication and requests with secure protocol (ie. HTTPS)
        if not port:
            port = self.port
        conn = httplib.HTTPConnection(self.host, port)
        self.log.debug("Host: {}:{}".format(self.host, self.port))
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        if authtoken:
            if self.x_subject_token:
                headers["X-Auth-Token"] = self.x_subject_token
        if post_data:
            method = "POST"
            headers["Content-type"] = "application/json"
            post_data = json.dumps(post_data)
            conn.request(method, url, post_data, headers=headers)
        elif delete_data:
            method = "DELETE"
            conn.request(method, url, json.dumps(delete_data), headers=headers)
        else:
            conn.request(method, url, headers=headers)
        resp = conn.getresponse()
        headers = resp.getheaders()
        try:
            self.x_subject_token = dict(headers)["x-subject-token"]
        except KeyError:
            pass
        content = resp.read()
        conn.close()
        if len(content) == 0:
            return {}
        try:
            content = json.loads(content)
            if "error" in content:
                try:
                    raise Exception("Getting an error while requiring {} ({}: {}, {})".format(
                        url,
                        content['error']['code'],
                        content['error']['title'],
                        content['error']['message'],
                    ))
                except ValueError:
                    raise Exception("Bad error format while requiring {} ({})".format(url, content))
            return content
        except ValueError:
            raise Exception("Getting an error while requiring {} ({})".format(url, content))
        finally:
            self.log.debug(str(content))

    def auth_keystone(self, username=None, password=None, host=None, port=None):
        """Send a new authentication request to Keystone

        :param username: user identification name
        :return:
        """
        if username:
            self.post["auth"]["identity"]["password"]["user"]["name"] = username
        if password:
            self.post["auth"]["identity"]["password"]["user"]["password"] = password
        if host:
            self.host = host
        if port:
            self.port = port
        data = self.get_url("/v3/auth/tokens", post_data=self.post)
        if "token" not in data:
            raise Exception("Authentication problem ({})".format(data))

    def initialize_app(self, argv):
        self.log.debug('initialize_app: {}'.format(argv))
        if self.options.username:
            self.post["auth"]["identity"]["password"]["user"]["name"] = self.options.username
            self.log.debug("change username {}".format(self.options.username))
        if self.options.password:
            self.post["auth"]["identity"]["password"]["user"]["password"] = self.options.password
            self.log.debug("change password")
        if self.options.tenant:
            self.post["auth"]["scope"]["project"]["name"] = self.options.tenant
            self._tenant_name = self.options.tenant
            self.log.debug("change tenant {}".format(self.options.tenant))
        if self.options.authurl:
            self.host = self.options.authurl.replace("https://", "").replace("http://", "").split("/")[0].split(":")[0]
            self.port = self.options.authurl.replace("https://", "").replace("http://", "").split("/")[0].split(":")[1]
            if "https" in self.options.authurl:
                self.secureprotocol = True
            else:
                self.secureprotocol = False
        data = self.get_url("/v3/auth/tokens", post_data=self.post)
        if "token" not in data:
            raise Exception("Authentication problem ({})".format(data))

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = MoonClient()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
