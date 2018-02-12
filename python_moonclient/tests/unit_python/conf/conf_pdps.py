from .conf_all import *

PDPS = {
    "pdps": {
        "1": {
                "name": "...",
                "security_pipeline": [],
                "keystone_project_id": "",
                "description": "...",
            }
        }
    }


POST_PDP = {
    "pdps": {
        "2": {
                "name": "test_pdp",
                "security_pipeline": [],
                "keystone_project_id": "",
                "description": "..."
            }
        }
    }

PATCH_PDP = {
    "pdps": {
        "2": {
                "name": "test_pdp",
                "security_pipeline": [],
                "keystone_project_id": "0c4e939acacf4376bdcd1129f1a054ad",
                "description": "..."
            }
        }
    }

PDPS_AFTER_POST = {
    "pdps": {
        "1": {
                "name": "...",
                "security_pipeline": [],
                "keystone_project_id": "",
                "description": "...",
            },

        "2": {
                "name": "test_pdp",
                "security_pipeline": [],
                "keystone_project_id": "",
                "description": "...",
            }
        }
    }

PDPS_AFTER_PATCH = {
    "pdps": {
        "1": {
                "name": "...",
                "security_pipeline": [],
                "keystone_project_id": "",
                "description": "...",
            },

        "2": {
                "name": "test_pdp",
                "security_pipeline": [],
                "keystone_project_id": "0c4e939acacf4376bdcd1129f1a054ad",
                "description": "...",
            }
        }
    }

def conf_pdps(m):
    m.register_uri(
        'GET', 'http://manager:30001/pdp',
        [{'json': PDPS, 'headers': {'X-Subject-Token': "111111111"}},
         {'json': PDPS_AFTER_POST, 'headers': {'X-Subject-Token': "111111111"}},
         {'json': PDPS_AFTER_PATCH, 'headers': {'X-Subject-Token': "111111111"}},
         {'json': PDPS, 'headers': {'X-Subject-Token': "111111111"}}]
    )
    m.register_uri(
        'POST', 'http://manager:30001/pdp',
        headers={'X-Subject-Token': "111111111"},
        json=POST_PDP
    )
    m.register_uri(
        'PATCH', 'http://manager:30001/pdp/2',
        headers={'X-Subject-Token': "111111111"},
        json=PATCH_PDP
    )
    m.register_uri(
        'DELETE', 'http://manager:30001/pdp/2',
        headers={'X-Subject-Token': "111111111"},
        json=RESULT_OK
    )