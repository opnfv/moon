## Welcome to the OPNFV/Opendaylight AAA Project!

This project is aimed at providing a flexible, pluggable framework with out-of-the-box capabilities for:

* *Authentication*:  Means to authenticate the identity of both human and machine users (direct or federated).
* *Authorization*:  Means to authorize human or machine user access to resources including RPCs, notification subscriptions, and subsets of the datatree.
* *Accounting*:  Means to record and access the records of human or machine user access to resources including RPCs, notifications, and subsets of the datatree



### Building

*Prerequisite:*  The followings are required for building AAA:

- Maven 3
- Java 7

Get the code:

    clone the project with git

Build it:

    cd aaa && mvn clean install -DskipTests

### Export Moon information

export MOON_SERVER_ADDR=192.168.56.101
export MOON_SERVER_PORT=5000


### Installing

AAA installs into an existing Opendaylight controller Karaf installation.  If you don't have an Opendaylight installation, please refer to this [page](https://wiki.opendaylight.org/view/OpenDaylight_Controller:Installation).

Start the controller Karaf container:
    cd distribution-karaf/target/assembly/
	bin/karaf

Install AAA AuthN features:

	feature:install odl-aaa-shiro

### Running

Once the installation finishes, one can authenticates with the Opendaylight controller by presenting a username/password and a domain name (scope) to be logged into:

    curl -s -d 'grant_type=password&username=admin&password=admin' http://<controller>:<port>/moon/token
    
    curl -s -d 'grant_type=password&username=admin&password=password' http://localhost:8080/moon/token

Upon successful authentication, the controller returns an access token with a configurable expiration in seconds, something similar to the followings:

    {"expires_in":3600,"token_type":"Bearer","access_token":"d772d85e-34c7-3099-bea5-cfafd3c747cb"}

The access token can then be used to access protected resources on the controller by passing it along in the standard HTTP Authorization header with the resource request.  Example:

    curl -s -H 'Authorization: Bearer d772d85e-34c7-3099-bea5-cfafd3c747cb' http://<controller>:<port>/restconf/operational/opendaylight-inventory:nodes

Test HTTP Basic Authentication

     curl -u admin:password http://localhost:8080/auth/v1/domains