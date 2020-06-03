# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.



def update_pdp(pdp_id, value):
    from moon_manager.db_driver import PDPManager
    return PDPManager.update_pdp("", pdp_id, value)


def delete_pdp(pdp_id):
    from moon_manager.db_driver import PDPManager
    PDPManager.delete_pdp("", pdp_id)


def add_pdp(pdp_id=None, value=None):
    from moon_manager.db_driver import PDPManager
    return PDPManager.add_pdp("", pdp_id, value)


def get_pdp(pdp_id=None):
    from moon_manager.db_driver import PDPManager
    return PDPManager.get_pdp("", pdp_id)
