# How-to develop on the Moon platform

## Install the platform

Follow the `moon/moonv4/README.md` file.

## GUI

The GUI code is located at `moon/moonv4/moon_gui`
The configuration values is at `moonv4/moon_gui/static/app/moon.constants.js`

To be able to only develop the GUI, you can install the Moon platform and run the GUI outside the platform.
To link the outside GUI to the Moon Manager, you must update the configuration values and specially the 
following variables :

- `{{MANAGER_HOST}}` : the hostname of the Manager (example: 127.0.0.1)
- `{{MANAGER_PORT}}` : the TCP port of the Manager (30001) 
- `{{KEYSTONE_HOST}}` : the hostname of the Keystone server (example: 127.0.0.1)
- `{{KEYSTONE_PORT}}` : the TCP port of the Keystone server (30006) 

To run the GUI service, follow the `README.md` file.

## Current bugs

1) ~~Models -> "`List of Meta rules`", after updating the meta_rule 
"`Actions` -> `edit`" and clicking on `close`, the main screen doesn't refresh~~

2) ~~idem if we want to remove the meta_rule~~

3) ~~after deleting an action perimeter (`Policy` -> `Add an action` -> `select a perimeter` and delete it), 
the dropdown list is not updated~~

4) ~~when adding a data subject (`Policy` -> `Data` -> `Add a Data Subject`), only the right category names must
be listed in `Catagory list`. Hide the categories that doesn't belong to that policy.~~

5) ~~idem for object data~~

6) ~~idem for action data~~

7) ~~after adding data (subject, object, action), the dropdown list in `Rules` -> `Add a rules` are not updated 
if the page is not manually refresh by the user and if the `Rules` window is already showing.~~

8) ~~typographic error in `Add a rules`~~

9) ~~in `Data` -> `Add a Data Object`, the `Create Data` never create the data in the backend~~

10) ~~Move the `project` tabular to the end~~

11) create a simplified version (to be discussed)
