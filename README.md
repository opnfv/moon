# Moon
__Version 5.4__
This directory contains all the modules for running the Moon platform.


## What is Moon

The Moon platform is a security policy engine with the following characteristics:

* centralized (or not)
  * Moon can centralize all authorization requests for multiple VIMs (Virtual Infrastructure Managers) at one time
  * Moon can centralize all security policies for multiple VIMs
  * with fully customizable security policies
* Moon can work on RBAC (Role based Access Control) policies or MLS (Multi Layer Security) policies
  * Moon can also create and use a new custom policy
* with a user centric management
  * The end user (administrator of the VIM) is able to generate his/her own policies and manage them

The Moon platform can also be a security orchestrator which can:

* dynamically assign and manage policies
* integrate OpenStack and OpenDaylight
* theorically integrate more systems (like VIMs, IoT, ...)

If you want to install the platform see [here](moon_manager/README.md)

## Software Architecture

Moon platform is composed on several API servers written in Python. Those servers can be installed on a bare metal system or on Docker, Kubernetes, OpenStack, ...

The communication between those servers is done by classic client/server connections (HTTP REST API) so the different components can be located on different and non homogenous systems.

The Moon platform is build on a plugins architecture so it is easy to customize the platform.

## Deployment Architecture

Moon is based on "Control Plane" and "Data Plane". The "Control Plane" manages the security policies, The "Data Plane" applies those policies.

![Moon planes](/docs/img/moon_planes.png)

Each project on a VIM will be connected to a specific PDP (Policy Decision Point) which is the main and the only entry point for this project.

The Moon "Control Plane" and "Data Planes" can be theoretically located everywhere as shown in the figure below:

![Moon planes overview](/docs/img/moon_planes2.png)

A "Data plane" could be located:

* in the same server as the "Control plane"
* in a totally different server
* in a virtual machine in an OpenStack VIM
* in a different server managing 2 different OpenStack

## Data Models

### Introduction

The Moon data model is based on a ABAC policy model (Attribute Based Access Control) which allow us to modeling every security policies.

When a connect like OpenStack need an authorization response, it sends to Moon a request with 3 elements (plus the project ID):

* the subject ID (user who do the action)
* the object ID (object which is the destination of the action)
* the action ID (action done by the user on the object)

For example, the "admin" (subject) wants to "start" (action) a specific virtual machine (object).

In the Moon data model, those elements are called "perimeter" elements.

To be able to write rules for authorization requests, the Moon data model uses 3 other elements, called "data".

For example, the role "admin" (subject) can do the action "start" (action) on a specific virtual machine (object).

The Moon data model objective is to 'map' perimeter elements with data elements given a specific data model.

![Moon data model](/docs/img/data_model.png)


### Examples

#### OpenStack

For example, the RBAC policy of OpenStack can be modeling with the following model:

* a user (perimeter subject) is mapped to a specific role (data subject)
* an virtual machine (perimeter object) is mapped to a specific ID (data object)
* an action, like "start a virtual machine" (perimeter action) is mapped to a specific ID (data action)

#### Multi Layer Security

The confidential defense, secret defense, ... policy (which are security level) could be modeling with a MLS policy like this:

* a user (perimeter subject) is linked to a specific security level (data subject)
* an virtual machine (perimeter object) is linked to a specific security level (data object)
* an action, like "start a virtual machine" (perimeter action) is linked to a specific ID (data action)

#### A more complex example

The Moon data model can be used to create more complex policies. For example, you need to set a different role for your users and you need also to tag them with a security level (high, medium and low). You also need to reduce the number of OpenStack commands to manage. At last, you need to reduce the number of managed objects and you want to tag each object with a security level. The model can be created with the following meta rule:

* the user name is linked to a role and to a security level
* the object ID is linked to a security level
* the action name is linked to a type of action

Here are some examples of data we can have in the perimeter items:

* subject: user_1, user_2, ...
* object: vm_1, vm_2, all_vm, glance_image_1, network_id1, ...
* action: compute:create, image_list, network::list, ...

Here are some examples of data we can have in the data items

* subject, role: admin, user, readonly, ...
* subject, security level: high, low
* object, security level: high, low
* action, type of action: nova_read, nova_write, glance_read, glance_write, neutron_read, ...

Linking perimeter with data is essential, in this example, we can have such assignments:

* subject, role: user_1 → admin
* subject, security level: user_1 → high
* subject, role: user_2 → admin
* subject, security level: user_1 → low
* object, security level: vm_1 → high
* object, security level: vm_2 → low
* object, security level: all_vm → low
* object, security level: glance_image_1 → low
* action, type of action: compute:create → nova_write
* action, type of action: image_list → glance_read
* action, type of action: network::list → neutron_read

At last, here are some examples of rules:

* (admin, high), (high), (nova_read)
* (admin, high), (high), (nova_write)
* (admin, low), (high), (nova_read)
* (admin, low), (low), (nova_read)
* (admin, low), (low), (nova_write)
* ...

## Components

The Moon platform is composed on 3 components:

* Manager
* Engine/Wrapper
* Engine/Pipeline

The first one can be considered as the master and the latest ones as slaves. Each components is a micro-service and is independent from other components.

![Moon components](/docs/img/components.png)

As shown in the previous diagram, the Manager manages several wrappers which can themselves manage several pipelines.

A more complete architecture applied for OpenStack can be this figure:

![Moon architecture](/docs/img/architecture.png)


### Manager

The manager is responsible of managing (read, write, delete) all data in the platform. It is connected to the main database (SQLite, MySQL, ...) and is the entry point for every requests concerning data inside the platform.

### Engine/Wrapper

The Wrapper is the entry point for the Manager to the slaves.

The main objective of the wrapper is to route every requests from the Manager or from the outside connector (like OpenStack, OpenDaylight, ...) to the correct Pipeline.

### Engine/Pipeline

The Pipeline contains the effective authorization engine of the Moon platform, if needed, it can work on its own without the need to contact the Manager. A user/developer can only use the engine if he/she doesn't need the whole Moon framework.

The Pipeline listen to requests from its dedicated wrapper or from outside connector, compute the result and send it back.

### Open Sourced

For the Open Source community, we released the following elements:

* a security policy engine
* a driver for
  * OpenStack
  * OpenDaylight
* a hook in Oslo_Policy (to be able to connect to external PDP)
* a web GUI integrated in the official OpenStack dashboard: Horizon

## Industrialization

Since 2018, a big effort has been done to transform the platform for industrialization requirements:

* Continuous integration with Gitlab-CI
* Project management with Jira
* Documentation management with Confluence

## Team

Actually the team is composed of:

* Administrative project leader: Philippe Calvez & Sok-Yen Loui (Orange)
* Technical project leader: Christophe Le Toquin (Orange)
* Consultant : Thomas Duval (Orange)
* Developpers:
    * Dimitri Darthenay (Orange)
    * Gregory Quere (Orange)

The Egypt team contract ended in march/april 2019.

