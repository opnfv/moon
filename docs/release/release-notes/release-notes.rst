.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ruan HE (Orange) and Thomas Duval (Orange)

Release Note for the Euphrates release of OPNFV when using Moon as a security management tool.

Abstract
========

This document provides the release notes for Euphrates release of Moon project.

Introduction
============

Moon is an OPNFV security management project which provides automated security management
toolset for OpenStack and other SDN controllers like OpenDaylight.
Please carefully follow the Installation Instructions to install and configure Moon.

Release Data
============

+--------------------------------------+--------------------------------------+
| **Project**                          | Moon                                 |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Repo/tag**                         | Moon/Euphrates.1.0                   |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release designation**              | Euphrates.1.0                        |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | September 2017                       |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Purpose of the delivery**          | OPNFV Euphrates release              |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Deliverables
------------

Software deliverables
~~~~~~~~~~~~~~~~~~~~~

Moon provides a security management framework for the OPNFV infrastructure.
It includes a set of software modules.

The internal software modules are:

 - keystone-moon: https://git.opnfv.org/cgit/moon/tree/moonv4

 - moonclient: https://git.opnfv.org/cgit/moon/tree/moonclient

 - tests: https://git.opnfv.org/cgit/moon/tree/tests


The OPNFV projects installs Moon is:

 * Compass4NFV


The OPNFV projects tests Moon are:

 * Functest

Documentation deliverables
~~~~~~~~~~~~~~~~~~~~~~~~~~

 - OPNFV(Euphrates) Moon installation instructions: http://artifacts.opnfv.org/moon/euphrates/docs/installationprocedure/index.html

 - OPNFV(Euphrates) Moon configuration guide: http://artifacts.opnfv.org/moon/euphrates/docs/configurationguide/index.html

 - OPNFV(Euphrates) Moon user guide: http://artifacts.opnfv.org/moon/euphrates/docs/userguide/index.html

Version change
--------------
.. This section describes the changes made since the last version of this document.

Feature evolution
~~~~~~~~~~~~~~~~~

This is the second tracked release of Moon

References
==========

For more information on the Moon Colorado release, please see:

https://wiki.opnfv.org/display/moon/