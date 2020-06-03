"""
intra_extensions = {
    intra_extension_id1: {
        name: xxx,
        model: yyy,
        description: zzz},
    intra_extension_id2: {...},
    ...
}

tenants = {
    tenant_id1: {
        name: xxx,
        description: yyy,
        intra_authz_extension_id: zzz,
        intra_admin_extension_id: zzz,
        },
    tenant_id2: {...},
    ...
}

--------------- for each intra-extension -----------------

subject_categories = {
    subject_category_id1: {
        name: xxx,
        description: yyy},
    subject_category_id2: {...},
    ...
}

subjects = {
    subject_id1: {
        name: xxx,
        description: yyy,
         ...},
    subject_id2: {...},
    ...
}

subject_scopes = {
    subject_category_id1: {
        subject_scope_id1: {
            name: xxx,
            description: aaa},
        subject_scope_id2: {
            name: yyy,
            description: bbb},
        ...},
        subject_scope_id3: {
        ...}
    subject_category_id2: {...},
    ...
}

subject_assignments = {
    subject_id1: {
        subject_category_id1: [subject_scope_id1, subject_scope_id2, ...],
        subject_category_id2: [subject_scope_id3, subject_scope_id4, ...],
        ...
    },
    subject_id2: {
        subject_category_id1: [subject_scope_id1, subject_scope_id2, ...],
        subject_category_id2: [subject_scope_id3, subject_scope_id4, ...],
        ...
    },
    ...
}

aggregation_algorithm = {
    aggregation_algorithm_id: {
         name: xxx,
         description: yyy
         }
    }

sub_meta_rules = {
    sub_meta_rule_id_1: {
        "name": xxx,
        "algorithm": yyy,
        "subject_categories": [subject_category_id1, subject_category_id2,...],
        "object_categories": [object_category_id1, object_category_id2,...],
        "action_categories": [action_category_id1, action_category_id2,...]
    sub_meta_rule_id_2: {...},
    ...
}

rules = {
    sub_meta_rule_id1: {
        rule_id1: [subject_scope1, subject_scope2, ..., action_scope1, ..., object_scope1, ... ],
        rule_id2: [subject_scope3, subject_scope4, ..., action_scope3, ..., object_scope3, ... ],
        rule_id3: [thomas, write, admin.subjects]
        ...},
    sub_meta_rule_id2: { },
    ...}
"""
