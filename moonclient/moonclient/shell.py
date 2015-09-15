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
    port = "35357"
    tenant = None
    _intraextension = None
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
        self.tenant = creds["tenant_name"]

    @property
    def intraextension(self):
        if not self._intraextension:
            self.log.debug("Setting intraextension")
            project_id = self.get_url("/v3/projects?name={}".format(self.tenant), authtoken=True)["projects"][0]["id"]
            self.log.debug("project_id={}".format(project_id))
            tenants = self.get_url("/v3/OS-MOON/tenants", authtoken=True)
            self.log.debug("tenants={}".format(tenants))
            if project_id not in tenants:
                self.log.info("Tenant [{}] was not added in Moon".format(project_id))
                return
            if tenants[project_id]['intra_authz_extension_id']:
                self._intraextension = tenants[project_id]['intra_authz_extension_id']
            elif tenants[project_id]['intra_admin_extension_id']:
                self._intraextension = tenants[project_id]['intra_admin_extension_id']
            else:
                self._intraextension = None
                self.log.info("No intra_extension found for tenant [{}].".format(project_id))
        return self._intraextension

    def get_tenant_uuid(self, tenant_name):
        return self.get_url("/v3/projects?name={}".format(tenant_name), authtoken=True)["projects"][0]["id"]

    def get_url(self, url, post_data=None, delete_data=None, method="GET", authtoken=None):
        if post_data:
            method = "POST"
        if delete_data:
            method = "DELETE"
        self.log.debug("\033[32m{} {}\033[m".format(method, url))
        conn = httplib.HTTPConnection(self.host, self.port)
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
        try:
            return json.loads(content)
        except ValueError:
            return {"content": content}

    def initialize_app(self, argv):
        self.log.debug('initialize_app: {}'.format(argv))
        # TODO: get credentials from OS env
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
