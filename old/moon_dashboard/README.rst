=============================================
Moon plugin for Horizon (OpenStack Dashboard)
=============================================

Install Horizon
===============

https://docs.openstack.org/horizon/latest/install/index.html

or for developper quick start:

https://docs.openstack.org/horizon/latest/contributor/quickstart.html


Moon plugin
=========== 

Clone the plugin:

"git clone https://gitlab.forge.orange-labs.fr/moon/dashboard.git"

* ``plugin`` is the location of moon plugin
* ``horizon`` is the location of horizon

Make symbolic link to enabled file:

"ln -s ``plugin`̀`/moon/enabled/_32000_moon.py ``horizon``/openstack_dashboard/local/enabled/_32000_moon.py"

Make symbolic link to dashboard folder:

"ln -s ``plugin`̀`/moon/ ``horizon``/openstack_dashboard/dashboards/moon"

Finish by restarting the Horizon server.


Set Moon API endpoint
===========

Set the endpoint in ``plugin``/moon/moon/static/moon/js/moon.module.js file