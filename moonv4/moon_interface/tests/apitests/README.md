Test directory
==============

API tests
---------
To test all interfaces, you can use :

```bash
$ cd moonv4/moon_interface/tests/apitests
$ pytest
============================================================================= test session starts ==============================================================================
platform linux -- Python 3.5.2, pytest-3.0.7, py-1.4.33, pluggy-0.4.0
rootdir: /home/vdsq3226/projets/opnfv/moonv4/moon_interface, inifile:
collected 15 items 

test_models.py .....
test_pdp.py .
test_policies.py .........

```

Populate default variables for a particular demonstration
---------------------------------------------------------

```bash
$ cd moonv4/moon_interface/tests/apitests
$ python3 populate_default_values.py scenario/rbac.py -v
Loading: scenario/rbac.py
2017-03-31 09:57:17,243 WARNING Creating model RBAC
2017-03-31 09:57:17,507 WARNING Creating policy Multi policy example
2017-03-31 09:57:18,690 WARNING Creating PDP pdp1

```