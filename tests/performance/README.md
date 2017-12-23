# Moon Yardstick and Bottlenecks Performance Tests

The main objective of this document is to describe the performance tests for the Moon project/module. 
Moon is a security managment platform which provides a set of security functions to project the underlying OPNFV infrastructure and/or VNFs. 
Moon is consisted of 2 parts: a master and a set of slaves. The master holds all security-related information and each slave only fetches and holds 
related informations for its local usage from master. 

## Moon Master Performance Tests
In this test, we should: 
- setup a Moon master service on a physical server 
- create a tenant/scope through the Moon master service
- create a MSL security policy with 4 subject security levels and 4 object security levels for this tenant

- increase N to find the limit of the security policy (implemented in format of a Docker)
  - create N users and N resources (VMs in our case) in this tenant
  - simulate 2 operation requests per user per second to Moon's authorization endpoint
  - gather performance metrics like CPU, memory, network usages
  - throught the iteration, determine the capacity limit for one Docker
  
- setup 20 user and 20 resources (VMs in our case) for one tenant
  - increase the number of tenants to test the maximal number of tenants on the server
  
- setup 5 tenants of N users and N resources (VMs in our case) in each tenant
  - increase N by simulating 2 operation requests per user per second to the Moon's authorization endpoint
  - gather performance metrics like CPU, memory, network usages
  - throught the iteration, dermine the maximal user/resource number of these 5 tenants/Dockers on the server

- setup 10 tenants of N users and N resources (VMs in our case) in each tenant
  - increase N by simulating 2 operation requests per user per second to the Moon's authorization endpoint
  - gather performance metrics like CPU, memory, network usages
  - throught the iteration, dermine the maximal user/resource number of these 10 tenants/Dockers on the server 

- setup 20 tenants of N users and N resources (VMs in our case) in each tenant
  - increase N by simulating 2 operation requests per user per second to the Moon's authorization endpoint
  - gather performance metrics like CPU, memory, network usages
  - throught the iteration, dermine the maximal user/resource number of these 20 tenants/Dockers on the server
  
## Moon Slave Performace Tests
In this test, we should: 
- setup a Moon master service on a physical server 
- setup a Moon slave service on a physical server 
- create a tenant/scope through the Moon master service
- create a MSL security policy with 4 subject security levels and 4 object security levels for this tenant through the Moon master service

- increase N to find the limit of the security policy (implemented in format of a Docker)
  - create N users and N resources (VMs in our case) in this tenant
  - simulate 2 operation requests per user per second to Moon slave's authorizatoin endpoint
  - gather performance metrics like CPU, memory, network usages of Moon slave
  - throught the iteration, dermine the capacity limit for one Docker of Moon slave
  
- setup 20 user and 20 resources (VMs in our case) for one tenant through the Moon slave service
  - increate the number of tenants to test the maximal number of tenants on the server of the Moon slave 
  
- setup 5 tenants of N users and N resources (VMs in our case) in each tenant through the Moon master service
  - increate N by simulating 2 operation requests per user per second to the Moon slave's authorization endpoint
  - gather performance metrics like CPU, memory, network usages of both Moon master and Moon slave
  - throught the iteration, dermine the maximal user/resource number of these 5 tenants/Dockers on the server of Moon slave

- setup 10 tenants of N users and N resources (VMs in our case) in each tenant through the Moon master service
  - increate N by simulating 2 operation requests per user per second to the Moon slave's authorization endpoint
  - gather performance metrics like CPU, memory, network usages of both Moon master and slave
  - throught the iteration, dermine the maximal user/resource number of these 10 tenants/Dockers on the server of the Moon slave

- setup 20 tenants of N users and N resources (VMs in our case) in each tenant through the Moon master service
  - increate N by simulating 2 operation requests per user per second to the Moon slave's authorization endpoint
  - gather performance metrics like CPU, memory, network usages of both Moon master and slave
  - throught the iteration, dermine the maximal user/resource number of these 20 tenants/Dockers on the server of the Moon slave


