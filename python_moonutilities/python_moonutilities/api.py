# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


class APIList(object):

    API_LIST = ()

    def __init__(self, api_list):
        self.API_LIST = api_list

    def list_api(self, ctx):
        api = dict()
        for obj in self.API_LIST:
            api[obj.__name__] = dict()
            api[obj.__name__]["description"] = obj.__doc__.strip() if obj.__doc__ else ""
            api[obj.__name__]["version"] = obj.__version__
            api[obj.__name__]["commands"] = dict()
            for cmd in filter(lambda x: not x.startswith("__"), dir(obj)):
                doc = eval("obj.{}.__doc__".format(cmd))
                if not doc:
                    doc = ""
                api[obj.__name__]["commands"][cmd] = doc.strip()
        return api


