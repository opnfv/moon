# GUI for the Moon project
This directory contains all the code for the Moon project
It is designed to provide a running GUI of the Moon platform instance.

## Usage
- Prerequist
  - `sudo apt-get install nodejs nodejs-legacy`
  - `sudo npm install --global gulp-cli`
- Install all packages 
  - `cd  $MOON_HOME/moon_gui`
  - `sudo npm install`
- Run the GUI
  - `gulp webServerDelivery`
  - Open your web browser

## Configuration
- build the delivery package: `gulp delivery`
- launch the Web Server: `gulp webServerDelivery`

## Development
- during the development it is possible to use following commands: `gulp build`
- launch a Web Server: `gulp webServer`
- Gulp webServer will refresh the browser when a file related to the application changed
- it is possible to change some constants (API endpoints): `$MOON_HOME/moon_gui/static/app/moon.constants.js`

## CORS
The GUI need to connect itself to Keystone and Moon.
Opening CORS to the GUI WebServer is required.
- modify Keystone: `$MOON_HOME/tools/moon_keystone/run.sh`
- modify Moon: `$MOON_HOME/moon_interface/interface/http_server.py`
 
## Usage
After authentication, you will see 4 tabs: Project, Models, Policies, PDP:

* *Projects*: configure mapping between Keystone projects and PDP (Policy Decision Point)
* *Models*: configure templates of policies (for example RBAC or MLS)
* *Policies*: applied models or instantiated models ; 
on one policy, you map a authorisation model and set subject, objects and action that will
rely on that model
* *PDP*: Policy Decision Point, this is the link between Policies and Keystone Project

In the following paragraphs, we will add a new user in OpenStack and allow her to list 
all VM on the OpenStack platform.

First, add a new user and a new project in the OpenStack platform:

      openstack user create --password-prompt demo_user
      openstack project create demo
      DEMO_USER=$(openstack user list | grep demo_user | cut -d " " -f 2)
      DEMO_PROJECT=$(openstack project list | grep demo | cut -d " " -f 2)
      openstack role add --user $DEMO_USER --project $DEMO_PROJECT admin
      
You have to add the same user in the Moon interface:

1. go to the `Projects` tab in the Moon interface
1. go to the line corresponding to the new project and click to the `Map to a PDP` link
1. select in the combobox the MLS PDP and click `OK`
1. in the Moon interface, go to the `Policy` tab
1. go to the line corresponding to the MLS policy and click on the `actions->edit` button
1. scroll to the `Perimeters` line and click on the `show` link to show the perimeter configuration
1. go to the `Add a subject` line and click on `Add a new perimeter`
1. set the name of that subject to `demo_user` (*the name must be strictly identical*)
1. in the combobox named `Policy list` select the `MLS` policy and click on the `+` button
1. click on the yellow `Add Perimeter` button
1. go to the `Assignment` line and click on the `show` button
1. under the `Add a Assignments Subject` select the MLS policy, 
the new user (`demo_user`), the category `subject_category_level` 
1. in the `Select a Data` line, choose the `High` scope and click on the `+` link 
1. click on the yellow `Create Assignments` button 
1. if you go to the OpenStack platform, the `demo_user` is now allow to connect 
to the Nova component (test with `openstack server list` connected with the `demo_user`)