#Moon Bouchon

Moon_bouchon is a fake interface to the Moon platform.
Moon platform can be requested through 2 interfaces:

- ''wrapper'', interface for the OpenStack platform
- ''interface'', interface for other components

## Usage:

### server

To start the server:

    docker run -ti -p 31002:31002 wukongsun/moon_bouchon:v1.0
    # or docker run -dti -p 31002:31002 wukongsun/moon_bouchon:v1.0

### wrapper

Here are the URL, you can request:
    
    POST /wrapper/authz/grant to request the wrapper component with always a "True" response 
    POST /wrapper/authz/deny to request the wrapper component with always a "False" response
    POST /wrapper/authz to request the wrapper component with always a "True" or "False" response

In each request you must pass the following data (or similar):

    {'rule': 'start', 'target': '{"target": {"name": "vm0"}, "user_id": "user0"}', 'credentials': 'null'}

You have examples in the moon_bouchon/tests directory.

### interface

Here are the URL, you can request:
    
    GET /interface/authz/grant/<string:project_id>/<string:subject_name>/<string:object_name>/<string:action_name> to request the interface component with always a "True" response 
    GET /interface/authz/deny/<string:project_id>/<string:subject_name>/<string:object_name>/<string:action_name> to request the interface component with always a "False" response
    GET /interface/authz/<string:project_id>/<string:subject_name>/<string:object_name>/<string:action_name> to request the interface component with always a "True" or "False" response

You have examples in the moon_bouchon/tests directory.


