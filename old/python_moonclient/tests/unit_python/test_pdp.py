from python_moonclient.core.pdp import *

def test_pdp():
    init("consul", 8500)
    projects = get_keystone_projects()
    admin_project_id = None
    for _project in projects['projects']:
        if _project['name'] == "admin":
            admin_project_id = _project['id']
    if admin_project_id is None:
        raise MoonCliException("Unexpected results, could not find the admin project")
    check_pdp()
    pdp_id = add_pdp()
    check_pdp(pdp_id)
    map_to_keystone(pdp_id=pdp_id, keystone_project_id=admin_project_id)
    check_pdp(pdp_id=pdp_id, keystone_project_id=admin_project_id)
    delete_pdp(pdp_id)
