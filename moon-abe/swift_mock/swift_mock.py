#!/usr/bin/env python3
"""<h1>Swift mock</h1>

<pre>

author: Thomas Duval

mail: thomas.duval@orange.com

version: 0.1

API:

- GET /info List activated capabilities

- GET /v1/{account} Show account details and list containers
- POST /v1/{account} Create, update, or delete account metadata
- HEAD /v1/{account} Show account metadata

- GET /v1/{account}/{container} Show container details and list objects
- PUT /v1/{account}/{container} Create container
- DELETE /v1/{account}/{container} Delete container
- POST /v1/{account}/{container} Create, update, or delete container metadata
- HEAD /v1/{account}/{container} Show container metadata

- GET /v1/{account}/{container}/{object} Get object content and metadata
- PUT /v1/{account}/{container}/{object} Create or replace object
- COPY /v1/{account}/{container}/{object} Copy object
- DELETE /v1/{account}/{container}/{object} Delete object
- COPY /v1/{account}/{container}/{object} Copy object
- HEAD /v1/{account}/{container}/{object} Show object metadata
- POST /v1/{account}/{container}/{object} Create or update object metadata
</pre>

<p>
Locally, the datastore is based on directories in /tmp/swift_dir,
those directories are built with the following structure:
{data_dir}/{account}/{container}/{object}.
</p>

<p>
For more information on SWIFT API:
<a href="http://developer.openstack.org/api-ref-objectstorage-v1.html">api-ref-objectstorage-v1.html</a>
</p>
"""
import cherrypy
import json
import os
import glob
import shutil
import time
import hashlib


TEMPLATE_HTML = """
<html>
<head><title>{title}</title></head>
<body>
{body}
</body>
</html>
"""


@cherrypy.popargs('account', 'container', 'object')
class Swift(object):

    def __init__(self):
        if os.path.isdir('/tmp'):
            self.data_dir = "/tmp/swift_data"
        else:
            self.data_dir = "data"
        cherrypy.log("Data dir set to {}".format(self.data_dir))
        try:
            os.mkdir(self.data_dir)
        except FileExistsError:
            cherrypy.log("Data dir already exist")

    def __get_json(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        return json.loads(rawbody.decode("utf-8"))

    def __get_rawdata(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        return rawbody

    @cherrypy.expose
    def index(self, account="", container="", object=""):
        return __doc__

    @cherrypy.expose
    def info(self, account="", container="", object=""):
        info_dict = {
            "swift": {
                "version": "1.11.0"
            },
            "staticweb": {},
            "tempurl": {}
        }
        return json.dumps(info_dict)

    @cherrypy.expose
    def v1(self, account="", container="", object=""):
        print("v1", account, container, object)
        if account and not container and not object:
            if cherrypy.request.method == "GET":
                return self.show_account(account)
            elif cherrypy.request.method == "POST":
                return self.create_account(account)
            elif cherrypy.request.method == "HEAD":
                return self.show_account_metadata(account)

        elif account and container and not object:
            if cherrypy.request.method == "GET":
                return self.show_container(account, container)
            elif cherrypy.request.method == "PUT":
                return self.create_container(account, container)
            elif cherrypy.request.method == "DELETE":
                return self.delete_container(account, container)
            elif cherrypy.request.method == "POST":
                return self.modify_container(account, container)
            elif cherrypy.request.method == "HEAD":
                return self.show_container_metadata(account, container)

        elif account and container and object:
            if cherrypy.request.method == "GET":
                return self.show_object(account, container, object)
            elif cherrypy.request.method == "PUT":
                return self.create_object(account, container, object)
            elif cherrypy.request.method == "DELETE":
                return self.delete_object(account, container, object)
            elif cherrypy.request.method == "COPY":
                return self.copy_object(account, container, object)
            elif cherrypy.request.method == "POST":
                return self.modify_object(account, container, object)
            elif cherrypy.request.method == "HEAD":
                return self.show_object_metadata(account, container, object)

        raise cherrypy.HTTPError(500, "Request not supported ({} - {})".format(
            cherrypy.request.method, cherrypy.request.query_string))

    def show_account(self, account):
        list_dir = glob.glob(os.path.join(self.data_dir, account, "*"))
        data_list = list()
        for _container in list_dir:
            _objects = glob.glob(os.path.join(self.data_dir, account, _container, "*"))
            data_list.append({
                "count": len(_objects),
                "bytes": 0,
                "name": os.path.basename(_container)
            })
        return json.dumps(data_list)

    def create_account(self, account):
        if not os.path.isdir(os.path.join(self.data_dir, account)):
            os.mkdir(os.path.join(self.data_dir, account))
            cherrypy.response.status = 204
            return "OK"
        raise cherrypy.HTTPError(500, "Account already created")

    def show_account_metadata(self, account):
        if not os.path.isdir(os.path.join(self.data_dir, account)):
            raise cherrypy.HTTPError(404)
        # TODO: header
        raise cherrypy.HTTPError(500, "Not implemented")

    def show_container(self, account, container):
        list_dir = glob.glob(os.path.join(self.data_dir, account, container, "*"))
        data_list = list()
        for _object in list_dir:
            data_list.append({
                "hash": hashlib.sha256(str.encode(_object)).hexdigest(),
                "last_modified": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(os.path.getmtime(_object))),
                "bytes": os.stat(_object).st_size,
                "name": os.path.basename(_object),
                "content_type": "application/octet-stream"
            })
        return json.dumps(data_list)

    def create_container(self, account, container):
        if not os.path.isdir(os.path.join(self.data_dir, account, container)):
            os.mkdir(os.path.join(self.data_dir, account, container))
            cherrypy.response.status = 204
            return
        raise cherrypy.HTTPError(500, "Container already created")

    def delete_container(self, account, container):
        if not os.path.isdir(os.path.join(self.data_dir, account, container)):
            raise cherrypy.HTTPError(404, "Container not found")
        try:
            os.rmdir(os.path.join(self.data_dir, account, container))
        except OSError:
            raise cherrypy.HTTPError(409, "Conflict")
        cherrypy.response.status = 204
        return "OK"
        # shutil.rmtree((os.path.join(self.data_dir, account)))

    def modify_container(self, account, container):
        # TODO: modifications in header
        return "modify_container {} {}".format(account, container)

    def show_container_metadata(self, account, container):
        if os.path.isdir(os.path.join(self.data_dir, account, container)):
            # TODO: modifications in header
            return "OK"
        raise cherrypy.HTTPError(404, "Container not found")

    def show_object(self, account, container, object):
        if os.path.isfile(os.path.join(self.data_dir, account, container, object)):
            # TODO: put metadata in headers
            return open(os.path.join(self.data_dir, account, container, object), "rb").read()
        raise cherrypy.HTTPError(404, "Object not found")

    def create_object(self, account, container, object):
        if not os.path.isdir(os.path.join(self.data_dir, account)):
            raise cherrypy.HTTPError(404, "Account not found")
        if not os.path.isdir(os.path.join(self.data_dir, account, container)):
            raise cherrypy.HTTPError(404, "Container not found")
        open(os.path.join(self.data_dir, account, container, object), "wb").write(self.__get_rawdata())
        cherrypy.response.status = 201
        return

    def delete_object(self, account, container, object):
        if not os.path.isfile(os.path.join(self.data_dir, account, container, object)):
            raise cherrypy.HTTPError(404, "Object not found")
        os.remove(os.path.join(self.data_dir, account, container, object))
        cherrypy.response.status = 204
        return

    def copy_object(self, account, container, object):
        if not os.path.isfile(os.path.join(self.data_dir, account, container, object)):
            raise cherrypy.HTTPError(404, "Object not found")
        # TODO: need to implement headers
        raise cherrypy.HTTPError(500, "Not implemented")

    def modify_object(self, account, container, object):
        # TODO headers
        raise cherrypy.HTTPError(500, "Not implemented")

    def show_object_metadata(self, account, container, object):
        # TODO headers
        raise cherrypy.HTTPError(500, "Not implemented")


application = Swift()

cherrypy.config.update({
    'server.socket_host': '127.0.0.1',
    'server.socket_port': 8080,
    })
cherrypy.quickstart(application)
