import itertools

""" an example of authz_buffer, sub_meta_rule_dict, rule_dict
authz_buffer = {
    'subject_uuid': xxx,
    'object_uuid': yyy,
    'action_uuid': zzz,
    'subject_attributes': {
        'subject_category1': [],
        'subject_category2': [],
        ...
        'subject_categoryn': []
    },
    'object_attributes': {},
    'action_attributes': {},
}

sub_meta_rule_dict = {
    "subject_categories": ["subject_security_level", "aaa"],
    "action_categories": ["computing_action"],
    "object_categories": ["object_security_level"],
}

rule_dict = [
    ["high", "vm_admin", "medium"],
    ["high", "vm_admin", "low"],
    ["medium", "vm_admin", "low"],
    ["high", "vm_access", "high"],
    ["high", "vm_access", "medium"],
    ["high", "vm_access", "low"],
    ["medium", "vm_access", "medium"],
    ["medium", "vm_access", "low"],
    ["low", "vm_access", "low"]
]
"""

def inclusion(authz_buffer, sub_meta_rule_dict, rule_dict):
    _cat = []
    for subject_cat in sub_meta_rule_dict['subject_categories']:
        if subject_cat in authz_buffer['subject_attributes']:
            _cat.append(authz_buffer['subject_attributes'][subject_cat])
    for action_cat in sub_meta_rule_dict['action_categories']:
        if action_cat in authz_buffer['action_attributes']:
            _cat.append(authz_buffer['action_attributes'][action_cat])
    for object_cat in sub_meta_rule_dict['object_categories']:
        if object_cat in authz_buffer['object_attributes']:
            _cat.append(authz_buffer['object_attributes'][object_cat])

    for _element in itertools.product(*_cat):
        if list(_element) in rule_dict:
            return True

    return False


def comparison(_authz_buffer, _sub_meta_rule_dict, _rule_dict):
    return


def all_true(decision_buffer):
    for _rule in decision_buffer:
        if decision_buffer[_rule] is False:
            return False
    return True