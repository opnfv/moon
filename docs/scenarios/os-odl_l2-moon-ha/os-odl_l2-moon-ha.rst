.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) ruan.he@orange.com & thomas.duval@orange.com


Introduction
============

This guide presents the use of the Moon platform.
The MoonClient script allows the administrator/user to drive the Moon platform and
some parts of the Keystone server itself.

Scenario components and composition
===================================

###Functional architecture
Moon can be considered as a management layer over OpenStack.
We can dynamically create security modules in Moon and assign these modules to protect different
tenants in OpenStack.
![](../img/moon_infra.png)

###Policy engine
The core part of the security management layer is its policy engine.
The policy engine should be at same time generic to support a large set of security models
used by consumers and robust so that all the manipulations on the policy engine need to be proved correct.
For all these purposes, we designed EMTAC (Extensible Multi-tenancy Access Control) meta-model,
which defines policy specification, policy administration, inter-policy collaboration and administration
over this collaboration.
![](../img/policy_engine.png)

###User-centric
At the same time, Moon enables administrators or a third-party application to define, configure and manage
its policies. Such a user-centric aspect helps users to define their own manner in using
OpenStack’s resources.

###Authorization enforcement in OpenStack
As the first step, the security policy in Moon is enforced by authorization mechanism in Keystone and Nova
and Swift.
All the operations in Keystone and Nova and Swift are controlled and validated by Moon.
In OpenStack, we implemented 3 hooks respectively for Keystone and Nova and Swift, the hooks will
redirect all authorization requests to Moon and return decision from Moon.

###Log System
Traceability and accountability are also handled in Moon, all the operations and interactions
are logged and can be consulted for any purpose.

###Separation of management layer from OpenStack
The separation of management layer from OpenStack makes the management system totally
independent from OpenStack. We can install Moon in client’s local so that Moon can be
locally administrated by clients and remotely project their data which are hosted in
Cloud Service Provider’s datacenter.

Scenario usage overview
=======================

The Moon platform is built on the OpenStack Keystone component. While Keystone manages the identification
and the authentication process, Moon manages the authorisation process for all actions that comes through it.
The current version of Moon can only manage a subset of actions: actions from Nova and Swift.
For example, when a user wanted to stop a virtual machine with Nova, the authorisation for that action of stopping
is delegated through KeystoneMiddleware to the Moon platform.

The MoonClient script helps administrators to configure the Moon platform and the authorisation rules.
It can be used like the OpenStack client with the same environment variables.

Each OpenStack project (or tenant) car be mapped to an intra-extension.
That intra-extension will contain the configuration for the authorisation process for that tenant.
Each intra-extension is configured with subjects, objects and actions. A subject makes an action on an object.
Those elements can be placed into categories, for example a subject can have a value on the role category.
Those values are saved into the scope element.
For example, the subject (which is also called user) "admin" can have the role "admin" and "dev" on the project "admin".
The same mapping applies to the object and the action element.
For example, the action "stop a VM" can be place in a particular category "access" with the scope "write".
The action "stop a VM" is considered as the user has a write access to the VM.

In order to grant or not an action in the system, Moon uses rules built with the scope values.
If we consider that a rule is constituted with a role for the subject category,
an ID and a security level for the object category and an access value for the action category, we can built rules
with values like the following ones:

- admin, id1, level_high, write
- admin, id1, level_low, read
- dev, id2, level_high, read

All configuration can be done with the MoonClient script.
If a project is not mapped to a intra-extension, it can be used as if the Moon platform doesn't exist.

Limitations, Issues and Workarounds
===================================

The Moon platform can only be used to authorize Nova and Swift actions. In future releases, it could manage
more OpenStack components like Neutron, Glance, ...

References
==========

For more information on the OPNFV Colorado release, please visit
http://www.opnfv.org/colorado

Revision: _sha1_

Build date: |today|
