# moon_manager

## Installation

```bash
python -m pip install moon_manager
sudo moon_manager_setup
```
If you want a development version:

```bash
ARTIFACTORY=https://artifactory-iva.si.francetelecom.fr/artifactory/api/pypi/python-virt-orange-product-devops/simple
sudo python -m pip install --pre moon_manager -i $ARTIFACTORY
```
Use it at your own risk, this is an unstable version.

If you want to be in development mode, and get the code, you can do the following steps:

```bash
git clone git@gitlab.forge.orange-labs.fr:moon/moon_utilities.git
cd moon_utilities
sudo pip install -r requirements.txt
sudo pip install -e .
cd ..
git clone git@gitlab.forge.orange-labs.fr:moon/moon_manager.git
cd moon_manager
sudo pip install -e .
```

## Configuration

A configuration file should be located in `/etc/moon/moon.yaml`, review it and update it to fit your needs.
You may need to change the following attributes:

* `debug`: true to false
* `database: url`: either sqlite or mysql
* `pwd_file`: put this file in a secured directory, this file contains the users and passwords of all the system
* `openstack: url`: the URL of the Keystone server (if used)

## Initialization

To initialize the database, use: 

```bash
moon_manager db
```

You need to add a new user (for example admin): 

```bash
moon_manager users add admin [-p admin_password]
```
If the password is not given, you will be prompt for one.

## Web server execution

For a development server, use:

```bash
hug -m moon_manager.server
```

For a production server:

If you use Information plugins, you must start the daemon (experimental):

```bash
moon_manager start_daemon 
```

Then, start the server and connect to the CLI with the `/etc/moon/moonrc` file:

```bash
moon_manager start_manager
. /etc/moon/moonrc admin admin
# Check if the service is up and running
moon_manager status --human
```

## Connect to API

* With a web browser
    1. go to http://127.0.0.1:8000/auth
    2. insert login and password (admin/admin for example)
    3. with "RestClient", "Postman" or an other Web API client add the "x-api-key" in headers with the key given by the previous step.
* With a console
    1. execute a basic auth to http://127.0.0.1:8000/auth
    2. use the received token to connect to API  
    
Example with httpie:

```bash
sudo python -m pip install httpie
http -a admin:admin 127.0.0.1:8000/auth
# copy the Token in TOKEN
http 127.0.0.1:8000/subjects "x-api-key:$TOKEN"
```

## Connect to HTML UI
You need to have `serve` installed on your server. To install it:

```
sudo apt install npm
sudo npm install -g serve
```

Then, configure the dashboard part of the `/etc/moon/moon.yaml` file like this:

```
dashboard:
root: <path to dist dir of moon gui>
pid_filename: <file to store the pid in, eg. /tmp/moon_web_ui.pid>
port: 8080
``` 

and:

```bash
moon_manager start_gui
```

Open your web browser and go to: http://127.0.0.1:8080/

The port can be changed in the conf file.
