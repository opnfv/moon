# Moon Jenkins
The aim of this repo is to give a quick way to start with jenkins in containers.
These were the aims of the automation:
- minimal interaction with Jenkins GUI - the plugins in plugins.txt are installed automatically, the admin user is setup based on environment variables, proxy variables are inherited from environment
- the build of the custom image is integrated in the same workflow

## Prerequisites
- one host running a newer version of the docker-engine
- docker-compose 1.18.0 

## Usage
- Setup secrets:
```bash
export JENKINS_USER=admin
export JENKINS_PASSWORD=admin
```
- Deploy jenkins:
```bash
docker-compose up -d
 ```
- Test: Jenkins GUI can be available on `http://<docker host IP>:8080`


## Pipeline Creation
You may find bellow an example of pipeline creation using BlueOcean interface.
As example I used a clone (https://github.com/brutus333/moon.git) of the moon project (https://git.opnfv.org/moon/)

Click on "Create a new job" in the classical Jenkins UI and follow the steps highlighted bellow:

![Create Multibranch Pipeline](images/Create%20Multibranch%20Pipeline.png)
![Select Source](images/Select%20Source%20Multibranch%20Pipeline.png)
![Configure Source](images/Git%20Source%20Multibranch%20Pipeline.png)
![Multibranch Pipeline Log](images/Multibranch%20Pipeline%20Log.png)

Clicking on BlueOcean shows the pipeline in the blueocean interface:

![Blue Ocean Pipeline success](images/blue%20ocean%20success%20pipeline.png)
