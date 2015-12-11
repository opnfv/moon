Moon API
========

Here are Moon API with some examples of posted data and returned data.

All requests must be prefexied by /v3/OS-MOON.

Authz
-----

**GET     /authz/{tenant_id}/{subject_k_id}/{object_name}/{action_name}**
  Authorization API.

.. code-block:: json

               return = {
                    "authz": "True or False"
               }


Intra-Extension API
-------------------

Configuration
~~~~~~~~~~~~~

**GET     /configuration/templates**

    List all policy templates.

.. code-block:: json

               return = {
                    "template_id": {
                        "name": "name of the template",
                        "description": "description of the template",
                    }
               }


**GET     /configuration/aggregation_algorithms**

    List all aggregation algorithms.

.. code-block:: json

               return = {
                    "algorithm_id": {
                        "name": "name of the algorithm",
                        "description": "description of the algorithm",
                    }
               }


**GET     /configuration/sub_meta_rule_algorithms**

    List all sub meta rule algorithms.

.. code-block:: json

               return = {
                    "algorithm_id": {
                        "name": "name of the algorithm",
                        "description": "description of the algorithm",
                    }
               }


Tenants
~~~~~~~

**GET     /tenants**

    List all tenants.

.. code-block:: json

               return = {
                    "tenant_id": {
                        "name": "name of the tenant",
                        "description": "description of the tenant",
                        "intra_authz_extension_id": "id of the intra extension authz",
                        "intra_admin_extension_id": "id of the intra extension authz"
                    }
               }


**POST    /tenants**

    Add a tenant.

.. code-block:: json

               post = {
                    "tenant_name": "name of the tenant",
                    "tenant_description": "description of the tenant",
                    "tenant_intra_authz_extension_id": "id of the intra extension authz",
                    "tenant_intra_admin_extension_id": "id of the intra extension admin"
               }
               return = {
                    "tenant_id": {
                        "name": "name of the tenant",
                        "description": "description of the tenant",
                        "intra_authz_extension_id": "id of the intra extension authz",
                        "intra_admin_extension_id": "id of the intra extension authz"
                    }
               }


**POST    /tenants/{tenant_id}**

    Show information of one tenant.

.. code-block:: json

               return = {
                    "tenant_id": {
                        "name": "name of the tenant",
                        "description": "description of the tenant",
                        "intra_authz_extension_id": "id of the intra extension authz",
                        "intra_admin_extension_id": "id of the intra extension authz"
                    }
               }


**POST    /tenants/{tenant_id}**

    Modify a tenant.

.. code-block:: json

               post = {
                    "tenant_name": "name of the tenant",
                    "tenant_description": "description of the tenant",
                    "tenant_intra_authz_extension_id": "id of the intra extension authz",
                    "tenant_intra_admin_extension_id": "id of the intra extension admin"
               }
               return = {
                    "tenant_id": {
                        "name": "name of the tenant",
                        "description": "description of the tenant",
                        "intra_authz_extension_id": "id of the intra extension authz",
                        "intra_admin_extension_id": "id of the intra extension authz"
                    }
               }


**DELETE  /tenants/{tenant_id}**

    Delete a tenant.

.. code-block:: json

               return = {}


Intra-Extension
~~~~~~~~~~~~~~~

**GET     /intra_extensions/init**

    Initialize the root Intra_Extension (if needed).

.. code-block:: json

               return = {}


**GET     /intra_extensions**

    List all Intra_Extensions.

.. code-block:: json

               return = {
                    "intra_extension_id": {
                        "name": "name of the intra extension",
                        "model": "model of the intra extension"
                    }
               }


**POST    /intra_extensions**

    Create a new Intra_Extension.

.. code-block:: json

               post = {
                    "intra_extension_name": "name of the intra extension",
                    "intra_extension_model": "model of the intra extension (taken from /configuration/templates)",
                    "intra_extension_description": "description of the intra extension",

               }
               return = {}


**GET     /intra_extensions/{intra_extension_id}/**

    Show details about one Intra_Extension.

.. code-block:: json

               return = {
                    "id": "intra_extension_id",
                    "name": "name of the intra extension",
                    "model": "model of the intra extension",
                    "genre": "genre of the intra extension",
                    "description": "model of the intra extension"
               }


**DELETE  /intra_extensions/{intra_extension_id}/**

    Delete an Intra_Extension.

.. code-block:: json

               return = {}


Intra-Extension Subjects
~~~~~~~~~~~~~~~~~~~~~~~~

**GET     /intra_extensions/{intra_extension_id}/subjects**

    List all subjects.

.. code-block:: json

               return = {
                    "subject_id": {
                        "name": "name of the subject",
                        "keystone_id": "keystone id of the subject"
                    }
               }


**POST    /intra_extensions/{intra_extension_id}/subjects**

    List all subjects.

.. code-block:: json

               post = {
                    "subject_name": "name of the subject",
                    "subject_description": "description of the subject",
                    "subject_password": "password for the subject",
                    "subject_email": "email address of the subject"
               }
               return = {
                    "subject_id": {
                        "name": "name of the subject",
                        "keystone_id": "keystone id of the subject"
                    }
               }


**DELETE  /intra_extensions/{intra_extension_id}/subjects/{subject_id}**

    Delete a subject.

.. code-block:: json

               return = {}


**GET     /intra_extensions/{intra_extension_id}/subject_categories**

    List all subject categories.

.. code-block:: json

               return = {
                    "subject_category_id": {
                        "name": "name of the category",
                        "description": "description of the category"
                    }
               }


**POST    /intra_extensions/{intra_extension_id}/subject_categories**

    Add a new subject category.

.. code-block:: json

               post = {
                    "subject_category_name": "name of the category",
                    "subject_category_description": "description of the category"
               }
               return = {
                    "subject_category_id": {
                        "name": "name of the category",
                        "description": "description of the category"
                    }
               }


**DELETE  /intra_extensions/{intra_extension_id}/subject_categories/{subject_category_id}**

    Delete a subject category.

.. code-block:: json

               return = {}


**GET     /intra_extensions/{intra_extension_id}/subject_scopes/{subject_category_id}**

    List all subject scopes for a specific subject category.

.. code-block:: json

               return = {
                    "subject_scope_id": {
                        "name": "name of the scope",
                        "description": "description of the scope"
                    }
               }


**POST    /intra_extensions/{intra_extension_id}/subject_scopes/{subject_category_id}**

    Add a new subject scope for a specific subject category.

.. code-block:: json

               post = {
                    "subject_scope_name": "name of the scope",
                    "subject_scope_description": "description of the scope"
               }
               return = {
                    "subject_scope_id": {
                        "name": "name of the scope",
                        "description": "description of the scope"
                    }
               }


**DELETE  /intra_extensions/{intra_extension_id}/subject_scopes/{subject_category_id}/{subject_scope_id}**

    Delete a subject scope.

.. code-block:: json

               return = {}


**GET     /intra_extensions/{intra_extension_id}/subject_assignments/{subject_id}/{subject_category_id}**

    List all subject assignments for a subject and for a subject category.

.. code-block:: json

               return = [
                    "subject_assignment_id1", "subject_assignment_id2"
               ]


**POST    /intra_extensions/{intra_extension_id}/subject_assignments**

    Add an assignment.

.. code-block:: json

               post = {
                    "subject_id": "id of the subject",
                    "subject_category_id": "id of the category",
                    "subject_scope_id": "id of the scope"
               }
               return = [
                    "subject_assignment_id1", "subject_assignment_id2"
               ]


**DELETE  /intra_extensions/{intra_extension_id}/subject_assignments/{subject_id}/{subject_category_id}/{subject_scope_id}**

    Delete a subject assignment.

.. code-block:: json

               return = {}


Intra-Extension Objects
~~~~~~~~~~~~~~~~~~~~~~~

**GET     /intra_extensions/{intra_extension_id}/objects**

    List all objects.

.. code-block:: json

               return = {
                    "object_id": {
                        "name": "name of the object",
                        "keystone_id": "keystone id of the object"
                    }
               }


**POST    /intra_extensions/{intra_extension_id}/objects**

    List all objects.

.. code-block:: json

               post = {
                    "object_name": "name of the object",
                    "object_description": "description of the object"
               }
               return = {
                    "object_id": {
                        "name": "name of the object",
                        "keystone_id": "keystone id of the object"
                    }
               }


**DELETE  /intra_extensions/{intra_extension_id}/objects/{object_id}**

    Delete a object.

.. code-block:: json

               return = {}


**GET     /intra_extensions/{intra_extension_id}/object_categories**

    List all object categories.

.. code-block:: json

               return = {
                    "object_category_id": {
                        "name": "name of the category",
                        "description": "description of the category"
                    }
               }


**POST    /intra_extensions/{intra_extension_id}/object_categories**

    Add a new object category.

.. code-block:: json

               post = {
                    "object_category_name": "name of the category",
                    "object_category_description": "description of the category"
               }
               return = {
                    "object_category_id": {
                        "name": "name of the category",
                        "description": "description of the category"
                    }
               }


**DELETE  /intra_extensions/{intra_extension_id}/object_categories/{object_category_id}**

    Delete a object category.

.. code-block:: json

               return = {}


**GET     /intra_extensions/{intra_extension_id}/object_scopes/{object_category_id}**

    List all object scopes for a specific object category.

.. code-block:: json

               return = {
                    "object_scope_id": {
                        "name": "name of the scope",
                        "description": "description of the scope"
                    }
               }


**POST    /intra_extensions/{intra_extension_id}/object_scopes/{object_category_id}**

    Add a new object scope for a specific object category.

.. code-block:: json

               post = {
                    "object_scope_name": "name of the scope",
                    "object_scope_description": "description of the scope"
               }
               return = {
                    "object_scope_id": {
                        "name": "name of the scope",
                        "description": "description of the scope"
                    }
               }


**DELETE  /intra_extensions/{intra_extension_id}/object_scopes/{object_category_id}/{object_scope_id}**

    Delete a object scope.

.. code-block:: json

               return = {}


**GET     /intra_extensions/{intra_extension_id}/object_assignments/{object_id}/{object_category_id}**

    List all object assignments for a object and for a object category.

.. code-block:: json

               return = [
                    "object_assignment_id1", "object_assignment_id2"
               ]


**POST    /intra_extensions/{intra_extension_id}/object_assignments**

    Add an assignment.

.. code-block:: json

               post = {
                    "object_id": "id of the object",
                    "object_category_id": "id of the category",
                    "object_scope_id": "id of the scope"
               }
               return = [
                    "object_assignment_id1", "object_assignment_id2"
               ]


**DELETE  /intra_extensions/{intra_extension_id}/object_assignments/{object_id}/{object_category_id}/{object_scope_id}**

    Delete a object assignment.

.. code-block:: json

               return = {}


Intra-Extension Actions
~~~~~~~~~~~~~~~~~~~~~~~

**GET     /intra_extensions/{intra_extension_id}/actions**

    List all actions.

.. code-block:: json

               return = {
                    "action_id": {
                        "name": "name of the action",
                        "keystone_id": "keystone id of the action"
                    }
               }


**POST    /intra_extensions/{intra_extension_id}/actions**

    List all actions.

.. code-block:: json

               post = {
                    "action_name": "name of the action",
                    "action_description": "description of the action",
                    "action_password": "password for the action",
                    "action_email": "email address of the action"
               }
               return = {
                    "action_id": {
                        "name": "name of the action",
                        "keystone_id": "keystone id of the action"
                    }
               }


**DELETE  /intra_extensions/{intra_extension_id}/actions/{action_id}**

    Delete a action.

.. code-block:: json

               return = {}


**GET     /intra_extensions/{intra_extension_id}/action_categories**

    List all action categories.

.. code-block:: json

               return = {
                    "action_category_id": {
                        "name": "name of the category",
                        "description": "description of the category"
                    }
               }


**POST    /intra_extensions/{intra_extension_id}/action_categories**

    Add a new action category.

.. code-block:: json

               post = {
                    "action_category_name": "name of the category",
                    "action_category_description": "description of the category"
               }
               return = {
                    "action_category_id": {
                        "name": "name of the category",
                        "description": "description of the category"
                    }
               }


**DELETE  /intra_extensions/{intra_extension_id}/action_categories/{action_category_id}**

    Delete a action category.

.. code-block:: json

               return = {}


**GET     /intra_extensions/{intra_extension_id}/action_scopes/{action_category_id}**

    List all action scopes for a specific action category.

.. code-block:: json

               return = {
                    "action_scope_id": {
                        "name": "name of the scope",
                        "description": "description of the scope"
                    }
               }


**POST    /intra_extensions/{intra_extension_id}/action_scopes/{action_category_id}**

    Add a new action scope for a specific action category.

.. code-block:: json

               post = {
                    "action_scope_name": "name of the scope",
                    "action_scope_description": "description of the scope"
               }
               return = {
                    "action_scope_id": {
                        "name": "name of the scope",
                        "description": "description of the scope"
                    }
               }


**DELETE  /intra_extensions/{intra_extension_id}/action_scopes/{action_category_id}/{action_scope_id}**

    Delete a action scope.

.. code-block:: json

               return = {}


**GET     /intra_extensions/{intra_extension_id}/action_assignments/{action_id}/{action_category_id}**

    List all action assignments for a action and for a action category.

.. code-block:: json

               return = [
                    "action_assignment_id1", "action_assignment_id2"
               ]


**POST    /intra_extensions/{intra_extension_id}/action_assignments**

    Add an assignment.

.. code-block:: json

               post = {
                    "action_id": "id of the action",
                    "action_category_id": "id of the category",
                    "action_scope_id": "id of the scope"
               }
               return = [
                    "action_assignment_id1", "action_assignment_id2"
               ]


**DELETE  /intra_extensions/{intra_extension_id}/action_assignments/{action_id}/{action_category_id}/{action_scope_id}**

    Delete a action assignment.

.. code-block:: json

               return = {}


Intra-Extension Rules
~~~~~~~~~~~~~~~~~~~~~

**GET     /intra_extensions/{intra_extension_id}/aggregation_algorithm**

    List aggregation algorithm for an intra extension.

.. code-block:: json

               return = {
                    "aggregation_algorithm_id": {
                        "name": "name of the aggregation algorithm",
                        "description": "description of the aggregation algorithm"
                    }
               }


**POST    /intra_extensions/{intra_extension_id}/aggregation_algorithm**

    Set the current aggregation algorithm for an intra extension.

.. code-block:: json

               post = {
                    "aggregation_algorithm_id": "id of the aggregation algorithm",
                    "aggregation_algorithm_description": "description of the aggregation algorithm"
               }
               return = {
                    "aggregation_algorithm_id": {
                        "name": "name of the aggregation algorithm",
                        "description": "description of the aggregation algorithm"
                    }
               }


**GET     /intra_extensions/{intra_extension_id}/sub_meta_rules**

    Show the current sub meta rules.

.. code-block:: json

               return = {
                    "sub_meta_rule_id": {
                        "name": "name of the aggregation algorithm",
                        "algorithm": "algorithm of the aggregation algorithm",
                        "subject_categories": ["subject_category_id1", "subject_category_id2"],
                        "object_categories": ["object_category_id1", "object_category_id2"],
                        "action_categories": ["action_category_id1", "action_category_id2"]
                    }
               }


.. code-block:: json

               return = {}


**GET     /intra_extensions/{intra_extension_id}/rule/{sub_meta_rule_id}**

    Set the current sub meta rule.

.. code-block:: json

               post = {
                    "sub_meta_rule_name": "name of the sub meta rule",
                    "sub_meta_rule_algorithm": "name of the sub meta rule algorithm",
                    "sub_meta_rule_subject_categories": ["subject_category_id1", "subject_category_id2"],
                    "sub_meta_rule_object_categories": ["object_category_id1", "object_category_id2"],
                    "sub_meta_rule_action_categories": ["action_category_id1", "action_category_id2"]
               }
               return = {}


**GET     /intra_extensions/{intra_extension_id}/rule/{sub_meta_rule_id}**

    List all rules.

.. code-block:: json

               return = {
                    "rule_id1": ["subject_scope_id1", "object_scope_id1", "action_scope_id1"],
                    "rule_id2": ["subject_scope_id2", "object_scope_id2", "action_scope_id2"]
               }


**POST    /intra_extensions/{intra_extension_id}/rule/{sub_meta_rule_id}**

    Add a new rule.

.. code-block:: json

               post = {
                    "subject_categories": ["subject_scope_id1"],
                    "object_categories": ["object_scope_id1"],
                    "action_categories": ["action_scope_id1"],
                    "enabled": True
               }
               return = {}


**DELETE  /intra_extensions/{intra_extension_id}/rule/{sub_meta_rule_id}/{rule_id}**

    Delete a rule.

.. code-block:: json

               return = {}


Logs
~~~~

**GET     /logs/{options}**

    List all logs.
    Options can be:

    * ``filter=<filter_characters>``
    * ``from=<show logs from this date>``
    * ``to=<show logs to this date>``
    * ``event_number=<get n logs>``

    Time format is '%Y-%m-%d-%H:%M:%S' (eg. "2015-04-15-13:45:20")

.. code-block:: json

               return = [
                    "2015-04-15-13:45:20 ...",
                    "2015-04-15-13:45:21 ...",
                    "2015-04-15-13:45:22 ...",
                    "2015-04-15-13:45:23 ..."
               ]

