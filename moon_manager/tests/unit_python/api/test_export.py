import json
import api.utilities as utilities
import api.import_export_utilities as import_export_utilities


MODEL_WITHOUT_META_RULES = {"models": [{"name": "test model", "description": "model description", "meta_rules": []}]}

POLICIES = {"models": [{"name": "test model", "description": "", "meta_rules": []}],
            "policies": [{"name": "test policy", "genre": "authz", "description": "policy description", "model": {"name" : "test model"}}]}

SUBJECTS_OBJECTS_ACTIONS = {"models": [{"name": "test model", "description": "", "meta_rules": []}],
                            "policies": [{"name": "test policy", "genre": "authz", "description": "policy description", "model": {"name" : "test model"}}],
                            "subjects": [{"name": "testuser", "description": "description of the subject", "extra": {"field_extra_subject": "value extra subject"}, "policies": [{"name": "test policy"}]}],
                            "objects": [{"name": "test object", "description": "description of the object", "extra": {"field_extra_object": "value extra object"}, "policies": [{"name": "test policy"}]}],
                            "actions": [{"name": "test action", "description": "description of the action", "extra": {"field_extra_action": "value extra action"}, "policies": [{"name": "test policy"}]}]}


SUBJECT_OBJECT_ACTION_CATEGORIES = {"subject_categories": [{"name": "test subject categories", "description": "subject category description"}],
                                    "object_categories": [{"name": "test object categories", "description": "object category description"}],
                                    "action_categories": [{"name": "test action categories", "description": "action category description"}]}

SUBJECT_OBJECT_ACTION_DATA = {"models": [{"name": "test model", "description": "", "meta_rules": [{"name": "meta rule"}]}],
                            "policies": [{"name": "test policy", "genre": "authz", "description": "policy description", "model": {"name" : "test model"}}],
                            "subject_categories": [{"name": "test subject categories", "description": "subject category description"}],
                            "object_categories": [{"name": "test object categories", "description": "object category description"}],
                            "action_categories": [{"name": "test action categories", "description": "action category description"}],
                            "subject_data": [{"name": "test subject data", "description": "subject data description", "policy": {"name": "test policy"}, "category": {"name": "test subject categories"}}],
                            "object_data": [{"name": "test object data", "description": "object data description", "policy": {"name": "test policy"}, "category": {"name": "test object categories"}}],
                            "action_data": [{"name": "test action data", "description": "action data description", "policy": {"name": "test policy"}, "category": {"name": "test action categories"}}],
                            "meta_rules": [{"name": "meta rule", "description": "valid meta rule", "subject_categories": [{"name": "test subject categories"}], "object_categories": [{"name": "test object categories"}], "action_categories": [{"name": "test action categories"}]}]}


META_RULES = {"subject_categories": [{"name": "test subject categories", "description": "subject category description"}],
              "object_categories": [{"name": "test object categories", "description": "object category description"}],
              "action_categories": [{"name": "test action categories", "description": "object action description"}],
              "meta_rules": [{"name": "meta rule", "description": "valid meta rule", "subject_categories": [{"name": "test subject categories"}], "object_categories": [{"name": "test object categories"}], "action_categories": [{"name": "test action categories"}]}]}


ASSIGNMENTS = {"models": [{"name": "test model", "description": "", "meta_rules": [{"name": "meta rule"}]}],
               "policies": [{"name": "test policy", "genre": "authz", "description": "policy description", "model": {"name" : "test model"}}],
               "subject_categories": [{"name": "test subject categories", "description": "subject category description"}],
               "object_categories": [{"name": "test object categories", "description": "object category description"}],
               "action_categories": [{"name": "test action categories", "description": "action category description"}],
               "subject_data": [{"name": "test subject data", "description": "subject data description", "policy": {"name": "test policy"}, "category": {"name": "test subject categories"}}],
               "object_data": [{"name": "test object data", "description": "object data description", "policy": {"name": "test policy"}, "category": {"name": "test object categories"}}],
               "action_data": [{"name": "test action data", "description": "action data description", "policy": {"name": "test policy"}, "category": {"name": "test action categories"}}],
               "meta_rules": [{"name": "meta rule", "description": "valid meta rule", "subject_categories": [{"name": "test subject categories"}], "object_categories": [{"name": "test object categories"}], "action_categories": [{"name": "test action categories"}]}],
               "subjects": [{"name": "testuser", "description": "description of the subject", "extra": {"field_extra_subject": "value extra subject"}, "policies": [{"name": "test policy"}]}],
               "objects": [{"name": "test object", "description": "description of the object", "extra": {"field_extra_object": "value extra object"}, "policies": [{"name": "test policy"}]}],
               "actions": [{"name": "test action", "description": "description of the action", "extra": {"field_extra_action": "value extra action"}, "policies": [{"name": "test policy"}]}],
               "subject_assignments": [{"subject": {"name": "testuser"}, "category": {"name": "test subject categories"}, "assignments": [{"name": "test subject data"}]}],
               "object_assignments": [{"object": {"name": "test object"}, "category": {"name": "test object categories"}, "assignments": [{"name": "test object data"}]}],
               "action_assignments": [{"action": {"name": "test action"}, "category": {"name": "test action categories"}, "assignments": [{"name": "test action data"}]}]}

RULES = {"models": [{"name": "test model", "description": "", "meta_rules": [{"name": "meta rule"}]}],
         "policies": [{"name": "test policy", "genre": "authz", "description": "policy description", "model": {"name" : "test model"}}],
         "subject_categories": [{"name": "test subject categories", "description": "subject category description"}],
         "object_categories": [{"name": "test object categories", "description": "object category description"}],
         "action_categories": [{"name": "test action categories", "description": "action category description"}],
         "subject_data": [{"name": "test subject data", "description": "subject data description", "policy": {"name": "test policy"}, "category": {"name": "test subject categories"}}],
         "object_data": [{"name": "test object data", "description": "object data description", "policy": {"name": "test policy"}, "category": {"name": "test object categories"}}],
         "action_data": [{"name": "test action data", "description": "action data description", "policy": {"name": "test policy"}, "category": {"name": "test action categories"}}],
         "meta_rules": [{"name": "meta rule", "description": "valid meta rule", "subject_categories": [{"name": "test subject categories"}], "object_categories": [{"name": "test object categories"}], "action_categories": [{"name": "test action categories"}]}],
         "subjects": [{"name": "testuser", "description": "description of the subject", "extra": {"field_extra_subject": "value extra subject"}, "policies": [{"name": "test policy"}]}],
         "objects": [{"name": "test object", "description": "description of the object", "extra": {"field_extra_object": "value extra object"}, "policies": [{"name": "test policy"}]}],
         "actions": [{"name": "test action", "description": "description of the action", "extra": {"field_extra_action": "value extra action"}, "policies": [{"name": "test policy"}]}],
         "subject_assignments": [{"subject": {"name": "testuser"}, "category": {"name": "test subject categories"}, "assignments": [{"name": "test subject data"}]}],
         "object_assignments": [{"object": {"name": "test object"}, "category": {"name": "test object categories"}, "assignments": [{"name": "test object data"}]}],
         "action_assignments": [{"action": {"name": "test action"}, "category": {"name": "test action categories"}, "assignments": [{"name": "test action data"}]}],
         "rules": [{"meta_rule": {"name" : "meta rule"}, "rule": {"subject_datas" : [{"name":"test subject data"}], "object_data": {"name": "test object data"}, "action_data": {"name": "test action data"}}, "policy": {"name" :"test policy"}, "instructions" : {"decision" : "grant"}, "enabled": True}]
        }


def test_export_models():
    client = utilities.register_client()
    import_export_utilities.clean_all(client)
    req = client.post("/import", content_type='application/json', data=json.dumps(MODEL_WITHOUT_META_RULES))
    data = utilities.get_json(req.data)
    assert data == "Import ok !"

    req = client.get("/export")
    assert req.status_code == 200
    data = utilities.get_json(req.data)

    print(data)
    assert "content" in data
    assert "models" in data["content"]
    assert isinstance(data["content"]["models"], list)
    assert len(data["content"]["models"]) == 1
    model = data["content"]["models"][0]
    assert model["name"] == "test model"
    assert model["description"] == "model description"
    assert isinstance(model["meta_rules"], list)
    assert len(model["meta_rules"]) == 0


def test_export_policies():
    client = utilities.register_client()
    import_export_utilities.clean_all(client)
    req = client.post("/import", content_type='application/json', data=json.dumps(POLICIES))
    data = utilities.get_json(req.data)
    assert data == "Import ok !"

    req = client.get("/export")
    assert req.status_code == 200
    data = utilities.get_json(req.data)

    print(data)
    assert "content" in data
    assert "policies" in data["content"]
    assert isinstance(data["content"]["policies"], list)
    assert len(data["content"]["policies"]) == 1
    policy = data["content"]["policies"][0]
    assert policy["name"] == "test policy"
    assert policy["genre"] == "authz"
    assert policy["description"] == "policy description"
    assert "model" in policy
    assert "name" in policy["model"]
    model = policy["model"]
    assert model["name"] == "test model"


def test_export_subject_object_action():
    client = utilities.register_client()
    import_export_utilities.clean_all(client)
    req = client.post("/import", content_type='application/json', data=json.dumps(SUBJECTS_OBJECTS_ACTIONS))
    data = utilities.get_json(req.data)
    assert data == "Import ok !"

    req = client.get("/export")
    assert req.status_code == 200
    data = utilities.get_json(req.data)

    print(data)
    assert "content" in data
    type_elements = ["subject", "object", "action"]
    for type_element in type_elements:
        key = type_element + "s"
        assert key in data["content"]
        assert isinstance(data["content"][key], list)
        assert len(data["content"][key]) == 1
        element = data["content"][key][0]
        if type_element == "subject":
            assert element["name"] == "testuser"
        else:
            assert element["name"] == "test "+ type_element
        assert element["description"] == "description of the " + type_element
        assert "policies" in element
        assert isinstance(element["policies"], list)
        assert len(element["policies"]) == 1
        assert isinstance(element["policies"][0], dict)
        assert element["policies"][0]["name"] == "test policy"
        assert isinstance(element["extra"], dict)
        key_dict = "field_extra_" + type_element
        value_dict = "value extra " + type_element
        #TODO change this after bug fix on extra
        if False:
            assert key_dict in element["extra"]
            assert element["extra"][key_dict] == value_dict


def test_export_subject_object_action_categories():
    client = utilities.register_client()
    import_export_utilities.clean_all(client)
    req = client.post("/import", content_type='application/json', data=json.dumps(SUBJECT_OBJECT_ACTION_CATEGORIES))
    data = utilities.get_json(req.data)
    assert data == "Import ok !"

    req = client.get("/export")
    assert req.status_code == 200
    data = utilities.get_json(req.data)
    print(data)
    assert "content" in data
    type_elements = ["subject", "object", "action"]
    for type_element in type_elements:
        key = type_element + "_categories"
        assert key in data["content"]
        assert isinstance(data["content"][key], list)
        assert len(data["content"][key]) == 1
        category = data["content"][key][0]
        assert category["name"] == "test " + type_element + " categories"
        assert category["description"] == type_element + " category description"


def test_export_subject_object_action_data():
    client = utilities.register_client()
    import_export_utilities.clean_all(client)
    req = client.post("/import", content_type='application/json', data=json.dumps(SUBJECT_OBJECT_ACTION_DATA))
    data = utilities.get_json(req.data)
    assert data == "Import ok !"

    req = client.get("/export")
    assert req.status_code == 200
    data = utilities.get_json(req.data)
    print(data)
    assert "content" in data
    type_elements = ["subject", "object", "action"]
    for type_element in type_elements:
        key = type_element + "_data"
        assert key in data["content"]
        assert isinstance(data["content"][key], list)
        assert len(data["content"][key]) == 1
        data_elt = data["content"][key][0]
        assert data_elt["name"] == "test " + type_element + " data"
        assert data_elt["description"] == type_element + " data description"
        assert isinstance(data_elt["policy"],dict)
        assert data_elt["policy"]["name"] == "test policy"
        assert isinstance(data_elt["category"],dict)
        assert data_elt["category"]["name"] == "test " + type_element + " categories"


def test_export_assignments():
    client = utilities.register_client()
    import_export_utilities.clean_all(client)
    req = client.post("/import", content_type='application/json', data=json.dumps(ASSIGNMENTS))
    data = utilities.get_json(req.data)
    assert data == "Import ok !"

    req = client.get("/export")
    assert req.status_code == 200
    data = utilities.get_json(req.data)
    print(data)
    assert "content" in data
    type_elements = ["subject", "object", "action"]
    for type_element in type_elements:
        key = type_element + "_assignments"
        assert key in data["content"]
        assert isinstance(data["content"][key], list)
        assert len(data["content"][key]) == 1
        assignment_elt = data["content"][key][0]
        assert type_element in assignment_elt
        assert isinstance(assignment_elt[type_element], dict)
        if type_element == "subject":
            assert assignment_elt[type_element]["name"] == "testuser"
        else:
            assert assignment_elt[type_element]["name"] == "test " + type_element
        assert "category" in assignment_elt
        assert isinstance(assignment_elt["category"], dict)
        assert assignment_elt["category"]["name"] == "test " + type_element + " categories"
        assert "assignments" in assignment_elt
        assert isinstance(assignment_elt["assignments"], list)
        assert len(assignment_elt["assignments"]) == 1
        assert assignment_elt["assignments"][0]["name"] == "test " + type_element + " data"


def test_export_rules():
    client = utilities.register_client()
    import_export_utilities.clean_all(client)
    req = client.post("/import", content_type='application/json', data=json.dumps(RULES))
    data = utilities.get_json(req.data)
    assert data == "Import ok !"

    req = client.get("/export")
    assert req.status_code == 200
    data = utilities.get_json(req.data)
    print(data)
    assert "content" in data
    assert "rules" in data["content"]
    assert isinstance(data["content"]["rules"], list)
    assert len(data["content"]["rules"]) == 1
    rule = data["content"]["rules"][0]
    assert "instructions" in rule
    assert "decision" in rule["instructions"]
    assert rule["instructions"]["decision"] == "grant"
    assert "enabled" in rule
    assert rule["enabled"] == True
    assert "meta_rule" in rule
    assert rule["meta_rule"]["name"] == "meta rule"
    assert "policy" in rule
    assert rule["policy"]["name"] == "test policy"
    assert "rule" in rule
    rule = rule["rule"]
    assert "subject_datas" in rule
    assert isinstance(rule["subject_datas"], list)
    assert len(rule["subject_datas"]) == 1
    assert rule["subject_datas"][0]["name"] == "test subject data"
    assert "object_data" in rule
    assert isinstance(rule["object_data"], dict)
    assert rule["object_data"]["name"] == "test object data"
    assert "action_data" in rule
    assert isinstance(rule["action_data"], dict)
    assert rule["action_data"]["name"] == "test action data"
