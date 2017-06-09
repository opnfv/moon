
GUI for the Moon project
================================

This directory contains all the code for the Moon project
It is designed to provide a running GUI of the Moon platform instance.


## Usage

### Prerequist
-   `sudo apt-get install nodejs nodejs-legacy`
-   `sudo npm install --global gulp-cli`


### Install all packages 
-   `cd  $MOON_HOME/moon_gui`
-   `sudo npm install`

### Run the GUI
-   `gulp webServerDelivery`
- Open your web browser


## Configuration

### Build the delivery package
-   `gulp delivery`
### Launch the Web Server
-   `gulp webServerDelivery`

### Development

During the development it is possible to use following commands :
-   `gulp build`
Launch a Web Server
-   `gulp webServer`
- Gulp webServer will refresh the browser when a file related to the application changed
  

### Constants
It is possible to change some constants (API endpoints)
- $MOON_HOME/moon_gui/static/app/moon.constants.js


### CORS

The GUI need to connect itself to Keystone and Moon.
Opening CORS to the GUI WebServer is required.

In order to modify Keystone :

`cd  $pathtoVmSpace/docker/keystone`

Concerned file is run.sh 

In order to modify Moon :

`cd  $MOON_HOME/moon_interface/interface`

Concerned file is http_server.py
 
 
