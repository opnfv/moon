#External Policy Checker

OpenStack component (like Nova, Glance, Cinder, ...) must populate 3 attributes to allow computing an authorization.
Those 3 attributes are:
- target
- credentials
- rule
In all those attributes, we must find the following information:
- In the 'credentials' attribute:
    - the user ID: this is given in general by Keystone
    - the project ID: this is given in general by Keystone
    - as a proposal, the domain ID: this is given in general by Keystone
- In the 'target' attribute:
    - the resource ID (ie nova virtual machine ID, Glance image ID, ...): this must come from the component source of the request (Nova, Glance, …)
- In the 'rule' attribute:
    - the action name: this must come from the component source of the request (Nova, Glance, )
    
This server must be used to verify that all information given from OpenStack components can be retrieved in those attributes.


## Usage:

### server

To start the server locally:
    
    cd external_policy_checker
    python3 server.py 

To start the server as a docker container:

    docker run -ti -p 8080:8080 moon_platform/external_policy_checker:latest

### API

Here are the API, you can request:
    
    POST /policy_checker 
    POST /authz/grant 
    POST /authz/deny

The `/policy_checker` allows to check if all information can be retrieve. 
The `/authz/grant` will always send a "True" response.
The `/authz/deny` will always send a "False" response.


