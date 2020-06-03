# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

def update_pdp(pdp_id, value):
    from python_moondb.core import PDPManager
    return PDPManager.update_pdp("", pdp_id, value)


def delete_pdp(pdp_id):
    from python_moondb.core import PDPManager
    PDPManager.delete_pdp("", pdp_id)


def add_pdp(pdp_id=None, value=None):
    from python_moondb.core import PDPManager
    return PDPManager.add_pdp("", pdp_id, value)


def get_pdp(pdp_id=None):
    from python_moondb.core import PDPManager
    return PDPManager.get_pdp("", pdp_id)
