# Moon Yardstick/Bottlenecks Performance Tests

The main objective of this document is to describe the performance tests for the Moon project/module. 
Moon is a security management platform which provides a set of security functions to project the underlying OPNFV infrastructure and/or VNFs. 
It is consisted of 2 parts: a master and a set of slaves. The master holds all security-related information and each slave only fetches and holds 
related information for its local usage from master. 

## Master Performance Tests
### Pre-requisite
- setup a Moon master service on a physical server 
- create a project in OpenStack/Keystone
- create a MSL PDP with a model of 4 subject security levels and 4 object security levels, the MLS policy will be defined later

### Policy Size Test
Increase the number of users and resources N to find the limit of the security policy
- create N users and N resources (VMs in our case) in this MLS security policy
- sends 5 authz requests/second
- gather performance metrics like CPU, memory, network usages
Through the iteration, determine the maximal number of N to support 5 requests/second 
  
### PDP Number Test  
- setup 20 user and 20 resources (VMs in our case) for each MLS PDP
- sends 5 authz requests/second for each MLS PDP
- increase the number of PDP to test the maximal number of PDP on the master
  
### Policy Size Test for 5 PDPs
- setup 5 PDPs of N users and N resources (VMs in our case)
- sends 5 authz requests/second for each MLS PDP
- gather performance metrics like CPU, memory, network usages
Through the iteration, determine the maximal user/resource number of these 5 PDPs

### Policy Size Test for 10 PDPs
- setup 10 PDPs of N users and N resources (VMs in our case)
- sends 5 authz requests/second for each MLS PDP
- gather performance metrics like CPU, memory, network usages
Through the iteration, determine the maximal user/resource number of these 10 PDPs

### Policy Size Test for 20 PDPs
- setup 20 PDPs of N users and N resources (VMs in our case)
- sends 5 authz requests/second for each MLS PDP
- gather performance metrics like CPU, memory, network usages
Through the iteration, determine the maximal user/resource number of these 20 PDPs


## Master-Slave Performance Tests
### Pre-requisite
- setup a Moon master on a physical server 
- setup a Moon slave on a physical server 
- create a project in OpenStack/Keystone
- create a MSL PDP with a model of 4 subject security levels and 4 object security levels, the MLS policy will be defined later on the master

### Slave Policy Size Test
Increase the number of users and resources N to find the limit of the security policy
- create N users and N resources (VMs in our case) in this MLS security policy on the master
- sends 5 authz requests/second to the slave
- gather performance metrics like CPU, memory, network usages of the slave
Through the iteration, determine the maximal number of N to support 5 requests/second of the slave 

### Slave PDP Number Test  
- setup 20 user and 20 resources (VMs in our case) for each MLS PDP on the master
- sends 5 authz requests/second for each MLS PDP to the slave
Through the iteration, determine the maximal number of PDP to support 5 requests/second of the slave

### Slave Policy Size Test for 5 PDPs
- setup 5 PDPs of N users and N resources (VMs in our case) on the master
- sends 5 authz requests/second for each MLS PDP to the slave
- gather performance metrics like CPU, memory, network usages of the slave
Through the iteration, determine the maximal user/resource number of these 5 PDPs

### Slave Policy Size Test for 10 PDPs
- setup 10 PDPs of N users and N resources (VMs in our case) on the master
- sends 5 authz requests/second for each MLS PDP to the slave
- gather performance metrics like CPU, memory, network usages of the slave
Through the iteration, determine the maximal user/resource number of these 10 PDPs

### Slave Policy Size Test for 20 PDPs
- setup 20 PDPs of N users and N resources (VMs in our case) on the master
- sends 5 authz requests/second for each MLS PDP to the slave
- gather performance metrics like CPU, memory, network usages of the slave
Through the iteration, determine the maximal user/resource number of these 20 PDPs
