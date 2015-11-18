# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import webob
import logging
import json
import re
import httplib

from cStringIO import StringIO
from oslo_config import cfg
from keystonemiddleware.i18n import _, _LC, _LE, _LI, _LW


_OPTS = [
    cfg.StrOpt('auth_uri',
               default="http://127.0.0.1:35357/v3",
               help='Complete public Identity API endpoint.'),
    cfg.StrOpt('auth_version',
               default=None,
               help='API version of the admin Identity API endpoint.'),
    cfg.StrOpt('keystonemiddleware_agent_logfile',  # TODO: update in the paste.ini
               default="/tmp/moon_keystonemiddleware_agent.log",
               help='File where logs goes.'),
    ]

_MOON_KEYSTONEMIDDLEWARE_AGENT_GROUP = 'moon_keystonemiddleware_agent'
CONF = cfg.CONF
CONF.register_opts(_OPTS, group=_MOON_KEYSTONEMIDDLEWARE_AGENT_GROUP)
CONF.debug = True

# from http://developer.openstack.org/api-ref-objectstorage-v1.html
SWIFT_API = (
    ("^/v1/(?P<account>[\w_-]+)$", "GET", "get_account_details"),
    ("^/v1/(?P<account>[\w_-]+)$", "POST", "modify_account"),
    ("^/v1/(?P<account>[\w_-]+)$", "HEAD", "get_account"),
    ("^/v1/(?P<account>[\w_-]+)/(?P<container>[\w-]+)$", "GET", "get_container"),
    ("^/v1/(?P<account>[\w_-]+)/(?P<container>[\w-]+)$", "PUT", "create_container"),
    ("^/v1/(?P<account>[\w_-]+)/(?P<container>[\w-]+)$", "POST", "update_container_metadata"),
    ("^/v1/(?P<account>[\w_-]+)/(?P<container>[\w-]+)$", "DELETE", "delete_container"),
    ("^/v1/(?P<account>[\w_-]+)/(?P<container>[\w-]+)$", "HEAD", "get_container_metadata"),
    ("^/v1/(?P<account>[\w_-]+)/(?P<container>[\w-]+)/(?P<object>.+)$", "GET", "get_object"),
    ("^/v1/(?P<account>[\w_-]+)/(?P<container>[\w-]+)/(?P<object>.+)$", "PUT", "create_object"),
    ("^/v1/(?P<account>[\w_-]+)/(?P<container>[\w-]+)/(?P<object>.+)$", "COPY", "copy_object"),
    ("^/v1/(?P<account>[\w_-]+)/(?P<container>[\w-]+)/(?P<object>.+)$", "POST", "update_object_metadata"),
    ("^/v1/(?P<account>[\w_-]+)/(?P<container>[\w-]+)/(?P<object>.+)$", "DELETE", "delete_object"),
    ("^/v1/(?P<account>[\w_-]+)/(?P<container>[\w-]+)/(?P<object>.+)$", "HEAD", "get_object_metadata"),
)


class MoonAgentKeystoneMiddleware(object):
    """Moon's agent for KeystoneMiddleware to interact calls."""

    post_data = {
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

    def __init__(self, app, conf):
        self.conf = conf
        self._LOG = logging.getLogger(conf.get('log_name', __name__))
        # FIXME: events are duplicated in log file
        moon_agent_fh = logging.FileHandler(CONF.moon_keystonemiddleware_agent["keystonemiddleware_agent_logfile"])
        self._LOG.setLevel(logging.DEBUG)
        self._LOG.addHandler(moon_agent_fh)
        self._LOG.info(_LI('Starting Moon KeystoneMiddleware Agent'))
        self._conf = conf
        self._app = app

        # Auth
        self.auth_host = conf.get('auth_host', "127.0.0.1")
        self.auth_port = int(conf.get('auth_port', 35357))
        auth_protocol = conf.get('auth_protocol', 'http')
        self._request_uri = '%s://%s:%s' % (auth_protocol, self.auth_host,  # TODO: ??? for  auth or authz
                                            self.auth_port)

        # SSL
        insecure = conf.get('insecure', False)
        cert_file = conf.get('certfile')
        key_file = conf.get('keyfile')

        if insecure:
            self._verify = False
        elif cert_file and key_file:
            self._verify = (cert_file, key_file)
        elif cert_file:
            self._verify = cert_file
        else:
            self._verify = None

        # Moon registered mgrs
        self.local_registered_mgr_dict = dict()  # TODO: load from the sql backend

    def __set_token(self):
        data = self.get_url("/v3/auth/tokens", post_data=self.post_data)
        if "token" not in data:
            raise Exception("Authentication problem ({})".format(data))
        self.token = data["token"]

    def __unset_token(self):
        data = self.get_url("/v3/auth/tokens", method="DELETE", authtoken=True)
        if "content" in data and len(data["content"]) > 0:
            self._LOG.error("Error while unsetting token {}".format(data["content"]))
        self.token = None

    def get_url(self, url, post_data=None, delete_data=None, method="GET", authtoken=None):
        if post_data:
            method = "POST"
        if delete_data:
            method = "DELETE"
        self._LOG.debug("\033[32m{} {}\033[m".format(method, url))
        conn = httplib.HTTPConnection(self.auth_host, self.auth_port)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        if authtoken:
            if self.x_subject_token:
                if method == "DELETE":
                    headers["X-Subject-Token"] = self.x_subject_token
                    headers["X-Auth-Token"] = self.x_subject_token
                else:
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

    def _find_openstack_component(self, env):
        if "nova.context" in env.keys():
            return "nova"
        elif "swift.authorize" in env.keys():
            return "swift"
        else:
            self._LOG.debug(env.keys())
            return "unknown"

    def _get_action(self, env, component):
        """ Find and return the action of the request
        Actually, find only Nova action (start, destroy, pause, unpause, ...)

        :param env: the request
        :return: the action or ""
        """
        action = ""
        self.input = ""
        if component == "nova":
            length = int(env.get('CONTENT_LENGTH', '0'))
            # TODO (dthom): compute for Nova, Cinder, Neutron, ...
            action = ""
            if length > 0:
                try:
                    sub_action_object = env['wsgi.input'].read(length)
                    self.input = sub_action_object
                    action = json.loads(sub_action_object).keys()[0]
                    body = StringIO(sub_action_object)
                    env['wsgi.input'] = body
                except ValueError:
                    self._LOG.error("Error in decoding sub-action")
                except Exception as e:
                    self._LOG.error(str(e))
            if not action or len(action) == 0 and "servers/detail" in env["PATH_INFO"]:
                return "list"
        if component == "swift":
            path = env["PATH_INFO"]
            method = env["REQUEST_METHOD"]
            for api in SWIFT_API:
                if re.match(api[0], path) and method == api[1]:
                    action = api[2]
            length = int(env.get('CONTENT_LENGTH', '0'))
            # TODO (dthom): compute for Nova, Cinder, Neutron, ...
            _action = ""
            if length > 0:
                try:
                    sub_action_object = env['wsgi.input'].read(length)
                    self.input = sub_action_object
                    _action = json.loads(sub_action_object).keys()[0]
                    body = StringIO(sub_action_object)
                    env['wsgi.input'] = body
                    self._LOG.debug("wsgi.input={}".format(_action))
                except ValueError:
                    self._LOG.error("Error in decoding sub-action")
                except Exception as e:
                    self._LOG.error(str(e))
        return action

    @staticmethod
    def _get_resource(env, component):
        if component == "nova":
            # http://developer.openstack.org/api-ref-compute-v2.1.html
            # nova URLs:
            #    /<tenant_id>/servers/<server_id>
            #       list details for server_id
            #    /<tenant_id>/servers/<server_id>/action
            #       execute action to server_id
            #    /<tenant_id>/servers/<server_id>/metadata
            #       show metadata from server_id
            #    /<tenant_id>/servers/details
            #       list servers
            url = env.get("PATH_INFO").split("/")
            if url[-1] == "detail":
                return "servers"
            try:
                return url[3]
            except IndexError:
                return
        elif component == "swift":
            # remove the "/v1/" part of the URL
            return env.get("PATH_INFO").split("/", 2)[-1].replace("/", "-").replace(".", "-")
        return "unknown"

    def __call__(self, env, start_response):
        req = webob.Request(env)
        agent_data = dict()

        agent_data['user_id'] = env.get("HTTP_X_USER_ID")
        if not agent_data['user_id']:
            self._LOG.warning("No user_id found for {}".format(env.get("PATH_INFO")))
            return self._app(env, start_response)

        agent_data['tenant_id'] = env.get("HTTP_X_TENANT_ID")
        if not agent_data['tenant_id']:
            self._LOG.warning("No tenant_id found for {}".format(env.get("PATH_INFO")))
            return self._app(env, start_response)

        agent_data['OS_component'] = self._find_openstack_component(env)

        agent_data['action_id'] = self._get_action(env, agent_data['OS_component'])
        if not agent_data['action_id']:
            self._LOG.warning("No action_id found for {}".format(env.get("PATH_INFO")))
            # If action is not found, we can't raise an exception because a lots of action is missing
            # in function self._get_action, it is not possible to get them all.
            return self._app(env, start_response)

        agent_data['resource_id'] = self._get_resource(env, agent_data['OS_component'])
        if not agent_data['resource_id'] :
            self._LOG.warning("No resource_id found for {}".format(env.get("PATH_INFO")))
            return self._app(env, start_response)
        else:
            self._LOG.debug("resource_id={}".format(agent_data['resource_id']))

        self.__set_token()
        for _mgr in self.local_registered_mgr_dict:  # TODO: update from the sql backend
            self.local_registered_mgr_dict[_mgr]['response_content'] = \
                json.loads(self.local_registered_mgr_dict[_mgr].treat_request(self.x_subject_token, agent_data).content)
        self.__unset_token()

        aggregate_result = 1
        for _mgr in self.local_registered_mgr_dict:
            if not self.local_registered_mgr_dict[_mgr]['response_content']:
                aggregate_result = 0

        if aggregate_result:
            return self._app(env, start_response)


def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)

    def moon_agent_filter(app):
        return MoonAgentKeystoneMiddleware(app, conf)
    return moon_agent_filter


