import logging
import requests
import six
import webob
import json

from keystone import exception
from keystonemiddleware.i18n import _, _LC, _LE, _LI, _LW
from oslo_config import cfg


_OPTS = [
    cfg.StrOpt('authz_mgr_login',
               default="admin",
               help='Name of the administrator who will connect to the Keystone Moon backends.'),
    cfg.StrOpt('authz_mgr_password',
               default="nomoresecrete",
               help='Password of the administrator who will connect to the Keystone Moon backends.'),
    cfg.StrOpt('authz_mgr_logfile',
               default="/tmp/moon_authz_mgr.log",  # TODO: update in paste.init
               help='File where logs goes.'),
    ]

_MOON_AUTHZ_MGR_GROUP = 'moon_authz_mgr'
CONF = cfg.CONF
CONF.register_opts(_OPTS, group=_MOON_AUTHZ_MGR_GROUP)
CONF.debug = True


class ServiceError(Exception):
    pass


class AuthzMgr(object):

    def __init__(self, conf):
        self._LOG = logging.getLogger(conf.get('log_name', __name__))
        authz_mgr_fh = logging.FileHandler(CONF.moon_authz_mgr["authz_mgr_logfile"])
        self._LOG.setLevel(logging.DEBUG)
        self._LOG.addHandler(authz_mgr_fh)

    def _deny_request(self, code):
        error_table = {
            'AccessDenied': (401, 'Access denied'),
            'InvalidURI': (400, 'Could not parse the specified URI'),
            'NotFound': (404, 'URI not found'),
            'Error': (500, 'Server error'),
        }
        resp = webob.Response(content_type='text/xml')
        resp.status = error_table[code][0]
        error_msg = ('<?xml version="1.0" encoding="UTF-8"?>\r\n'
                     '<Error>\r\n  <Code>%s</Code>\r\n  '
                     '<Message>%s</Message>\r\n</Error>\r\n' %
                     (code, error_table[code][1]))
        if six.PY3:
            error_msg = error_msg.encode()
        resp.body = error_msg
        return resp


    def treat_request(self, auth_token, agent_data):
        if not agent_data['resource_id']:
            agent_data['resource_id'] = "servers"

        headers = {'X-Auth-Token': auth_token}
        self._LOG.debug('X-Auth-Token={}'.format(auth_token))
        try:
            _url ='{}/v3/OS-MOON/authz/{}/{}/{}/{}'.format(
                                        self._request_uri,
                                        agent_data['tenant_id'],
                                        agent_data['user_id'],
                                        agent_data['resource_id'],
                                        agent_data['action_id'])
            self._LOG.info(_url)
            response = requests.get(_url,
                                    headers=headers,
                                    verify=self._verify)
        except requests.exceptions.RequestException as e:
            self._LOG.error(_LI('HTTP connection exception: %s'), e)
            resp = self._deny_request('InvalidURI')
            raise ServiceError(resp)

        if response.status_code < 200 or response.status_code >= 300:
            self._LOG.debug('Keystone reply error: status=%s reason=%s',
                               response.status_code, response.reason)
            if response.status_code == 404:
                resp = self._deny_request('NotFound')
            elif response.status_code == 401:
                resp = self._deny_request('AccessDenied')
            else:
                resp = self._deny_request('Error')
            raise ServiceError(resp)

        elif response.status_code == 200:
            answer = json.loads(response.content)
            self._LOG.debug("action_id={}/{}".format(agent_data['OS_component'] , agent_data['action_id']))
            self._LOG.debug(answer)
            if "authz" in answer and answer["authz"]:
                return response
            self._LOG.error("You are not authorized to do that! ({})".format(unicode(answer["comment"])))
            raise exception.Unauthorized(message="You are not authorized to do that! ({})".format(unicode(answer["comment"])))
        else:
            self._LOG.error("Unable to request Moon ({}: {})".format(response.status_code, response.reason))

        return response
