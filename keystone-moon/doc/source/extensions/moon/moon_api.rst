Moon API
========

Here are Moon API with some examples of posted data and returned data.

Intra-Extension API
-------------------

Authz
~~~~~

* ``GET     /OS-MOON/authz/{tenant_id}/{subject_id}/{object_id}/{action_id}``

.. code-block:: json

               return = {
                            "authz": "OK/KO/OutOfScope",
                            "tenant_id": "tenant_id",
                            "subject_id": "subject_id",
                            "object_id": "object_id",
                            "action_id": "action_id"
                        }

Intra_Extension
~~~~~~~~~~~~~~~

* ``GET     /OS-MOON/authz_policies``

.. code-block:: json

               return = {
                            "authz_policies": ["policy_name1", "policy_name2"]
                        }

* ``GET     /OS-MOON/intra_extensions``

.. code-block:: json

               return = {
                            "intra_extensions": ["ie_uuid1", "ie_uuid2"]
                        }

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}``

.. code-block:: json

               return = {
                            "intra_extensions": {
                                "id": "uuid1",
                                "description": "",
                                "tenant": "tenant_uuid",
                                "model": "",
                                "genre": "",
                                "authz": {},
                                "admin": {}
                            }
                        }

* ``POST    /OS-MOON/intra_extensions``

.. code-block:: json

                 post = {
                            "name" : "",
                            "policymodel": "",
                            "description": ""
                        }
               return = {
                            "id": "uuid1",
                            "description": "",
                            "tenant": "tenant_uuid",
                            "model": "",
                            "genre": "",
                            "authz": {},
                            "admin": {}
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}``

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/tenant``

.. code-block:: json

               return = {
                            "tenant": "tenant_id"
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/tenant``

.. code-block:: json

                 post = {
                            "tenant_id": "tenant_id"
                        }
               return = {
                            "tenant": "tenant_id"
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/tenant/{tenant_id}``

Perimeter
~~~~~~~~~

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/subjects``

.. code-block:: json

               return = {
                            "subjects": ["sub_uuid1", "sub_uuid2"]
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/subjects``

.. code-block:: json

                 post = {
                            "subject_id" : ""
                        }
               return = {
                            "subjects": ["sub_uuid1", "sub_uuid2"]
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/subject/{subject_id}``

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/objects``

.. code-block:: json

               return = {
                            "objects": ["obj_uuid1", "obj_uuid2"]
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/objects``

.. code-block:: json

                 post = {
                            "object_id" : ""
                        }
               return = {
                            "objects": ["obj_uuid1", "obj_uuid2"]
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/object/{object_id}``

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/actions``

.. code-block:: json

               return = {
                            "actions": ["act_uuid1", "act_uuid2"]
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/actions``

.. code-block:: json

                 post = {
                            "action_id" : ""
                        }
               return = {
                            "actions": ["act_uuid1", "act_uuid2"]
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/actions/{action_id}``

Assignment
~~~~~~~~~~

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/subject_assignments``

.. code-block:: json

               return = {
                            "subject_assignments": {
                                "subject_security_level":{
                                    "user1": ["low"],
                                    "user2": ["medium"],
                                    "user3": ["high"]
                            }
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/subject_assignments``

.. code-block:: json

                 post = {
                            "subject_id" : "",
                            "subject_category_id" : "",
                            "subject_category_scope_id" : ""
                        }
               return = {
                            "subject_assignments": {
                                "subject_security_level":{
                                    "user1": ["low"],
                                    "user2": ["medium"],
                                    "user3": ["high"]
                            }
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/subject_assignments/{subject_category}/{subject_id}/{subject_scope}``

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/object_assignments``

.. code-block:: json

               return = {
                            "object_assignments": {
                                "object_security_level":{
                                    "vm1": ["low"],
                                    "vm2": ["medium"],
                                    "vm3": ["high"]
                            }
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/object_assignments``

.. code-block:: json

                 post = {
                            "object_id" : "",
                            "object_category_id" : "",
                            "object_category_scope_id" : ""
                        }
               return = {
                            "object_assignments": {
                                "object_security_level":{
                                    "vm1": ["low"],
                                    "vm2": ["medium"],
                                    "vm3": ["high"]
                            }
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/object_assignments/{object_category}/{object_id}/{object_scope}``

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/action_assignments``

.. code-block:: json

               return = {
                            "action_assignments": {
                                "computing_action":{
                                    "pause": ["vm_admin"],
                                    "unpause": ["vm_admin"],
                                    "start": ["vm_admin"],
                                    "stop": ["vm_admin"]
                            }
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/action_assignments``

.. code-block:: json

                 post = {
                            "action_id" : "",
                            "action_category_id" : "",
                            "action_category_scope_id" : ""
                        }
               return = {
                            "action_assignments": {
                                "computing_action":{
                                    "pause": ["vm_admin"],
                                    "unpause": ["vm_admin"],
                                    "start": ["vm_admin"],
                                    "stop": ["vm_admin"]
                            }
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/action_assignments/{action_category}/{action_id}/{action_scope}``

Metadata
~~~~~~~~

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/subject_categories``

.. code-block:: json

               return = {
                            "subject_categories": [ "subject_security_level" ]
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/subject_categories``

.. code-block:: json

                 post = {
                            "subject_category_id" : ""
                        }
               return = {
                            "subject_categories": [ "subject_security_level" ]
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/subject_categories/{subject_category_id}``

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/object_categories``

.. code-block:: json

               return = {
                            "object_categories": [ "object_security_level" ]
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/object_categories``

.. code-block:: json

                 post = {
                            "object_category_id" : ""
                        }
               return = {
                            "object_categories": [ "object_security_level" ]
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/object_categories/{object_category_id}``

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/action_categories``

.. code-block:: json

               return = {
                            "action_categories": [ "computing_action" ]
                        }


* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/action_categories``

.. code-block:: json

                 post = {
                            "action_category_id" : ""
                        }
               return = {
                            "action_categories": [ "computing_action" ]
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/action_categories/{action_category_id}``

Scope
~~~~~

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/subject_category_scope``

.. code-block:: json

               return = {
                            "subject_security_level": [ "high", "medium", "low" ]
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/subject_category_scope``

.. code-block:: json

                 post = {
                            "subject_category_id" : "",
                            "subject_category_scope_id" : ""
                        }
               return = {
                            "subject_security_level": [ "high", "medium", "low" ]
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/subject_category_scope/{subject_category}/{subject_scope}``

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/object_category_scope``

.. code-block:: json

               return = {
                            "object_security_level": [ "high", "medium", "low" ]
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/object_category_scope``

.. code-block:: json

                 post = {
                            "object_category_id" : "",
                            "object_category_scope_id" : ""
                        }
               return = {
                            "object_security_level": [ "high", "medium", "low" ]
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/object_category_scope/{object_category}/{object_scope}``

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/action_category_scope``

.. code-block:: json

               return = {
                            "computing_action": [ "vm_admin", "vm_access" ]
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/action_category_scope``

.. code-block:: json

                 post = {
                            "action_id" : "",
                            "action_category_id" : "",
                            "action_category_scope_id" : ""
                        }
               return = {
                            "computing_action": [ "vm_admin", "vm_access" ]
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/action_category_scope/{action_category}/{action_scope}``

Metarule
~~~~~~~~

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/aggregation_algorithms``

.. code-block:: json

               return = {
                            "aggregation_algorithms": [ "and_true_aggregation", "..."]
                        }

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/aggregation_algorithm``

.. code-block:: json

               return = {
                            "aggregation_algorithm": "and_true_aggregation"
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/aggregation_algorithm``

.. code-block:: json

                 post = {
                            "aggregation": "and_true_aggregation"
                        }
               return = {
                            "aggregation_algorithm": "and_true_aggregation"
                        }

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/sub_meta_rule``

.. code-block:: json

               return = {
                            "sub_meta_rule": {
                                "subject_categories": ["role"],
                                "action_categories": ["ie_action"],
                                "object_categories": ["id"],
                                "relation": "relation_super"
                            }
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/sub_meta_rule``

.. code-block:: json

                 post = {
                            "relation_super": {
                                "subject_categories": ["role"],
                                "action_categories": ["ie_action"],
                                "object_categories": ["id"],
                            }
                        }
               return = {
                            "sub_meta_rule": {
                                "subject_categories": ["role"],
                                "action_categories": ["ie_action"],
                                "object_categories": ["id"],
                                "relation": "relation_super"
                            }
                        }

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/sub_meta_rule_relations``

.. code-block:: json

               return = {
                            "sub_meta_rule_relations": ["relation_super", ]
                        }

Rules
~~~~~

* ``GET     /OS-MOON/intra_extensions/{intra_extensions_id}/sub_rules``

.. code-block:: json

               return = {
                            "sub_rules": {
                                  "relation_super": [
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
                            }
                        }

* ``POST    /OS-MOON/intra_extensions/{intra_extensions_id}/sub_rules``

.. code-block:: json

                 post = {
                            "rules": ["admin", "vm_admin", "servers"],
                            "relation": "relation_super"
                        }

* ``DELETE  /OS-MOON/intra_extensions/{intra_extensions_id}/sub_rules/{relation_name}/{rule}``


Tenant mapping API
------------------

* ``GET  /OS-MOON/tenants``

.. code-block:: json

               return = {
                            "tenant": {
                                "uuid1": {
                                    "name": "tenant1",
                                    "authz": "intra_extension_uuid1",
                                    "admin": "intra_extension_uuid2"
                                },
                                "uuid2": {
                                    "name": "tenant2",
                                    "authz": "intra_extension_uuid1",
                                    "admin": "intra_extension_uuid2"
                                }
                            }
                        }

* ``GET  /OS-MOON/tenant/{tenant_uuid}``

.. code-block:: json

               return = {
                            "tenant": {
                                "uuid": {
                                    "name": "tenant1",
                                    "authz": "intra_extension_uuid1",
                                    "admin": "intra_extension_uuid2"
                                }
                            }
                        }

* ``POST  /OS-MOON/tenant``

.. code-block:: json

                 post = {
                            "id": "uuid",
                            "name": "tenant1",
                            "authz": "intra_extension_uuid1",
                            "admin": "intra_extension_uuid2"
                        }
               return = {
                            "tenant": {
                                "uuid": {
                                    "name": "tenant1",
                                    "authz": "intra_extension_uuid1",
                                    "admin": "intra_extension_uuid2"
                                }
                            }
                        }

* ``DELETE  /OS-MOON/tenant/{tenant_uuid}/{intra_extension_uuid}``

.. code-block:: json

               return = {}

Logs API
--------

* ``GET  /OS-MOON/logs``

InterExtension API
------------------

* ``GET     /OS-MOON/inter_extensions``

.. code-block:: json

               return = {
                            "inter_extensions": ["ie_uuid1", "ie_uuid2"]
                        }

* ``GET     /OS-MOON/inter_extensions/{inter_extensions_id}``

.. code-block:: json

               return = {
                            "inter_extensions": {
                                "id": "uuid1",
                                "description": "",
                                "requesting_intra_extension_uuid": "uuid1",
                                "requested_intra_extension_uuid": "uuid2",
                                "genre": "trust_OR_coordinate",
                                "virtual_entity_uuid": "ve_uuid1"
                            }
                        }

* ``POST    /OS-MOON/inter_extensions``

.. code-block:: json

                 post = {
                            "description": "",
                            "requesting_intra_extension_uuid": uuid1,
                            "requested_intra_extension_uuid": uuid2,
                            "genre": "trust_OR_coordinate",
                            "virtual_entity_uuid": "ve_uuid1"
                        }
               return = {
                            "id": "uuid1",
                            "description": "",
                            "requesting_intra_extension_uuid": uuid1,
                            "requested_intra_extension_uuid": uuid2,
                            "genre": "trust_OR_coordinate",
                            "virtual_entity_uuid": "ve_uuid1"
                        }

* ``DELETE  /OS-MOON/inter_extensions/{inter_extensions_id}``

