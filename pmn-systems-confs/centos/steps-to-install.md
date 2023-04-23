# PMN-SYSTEMS CENTOS INSTALLATION

## Prepare the system
* cd /etc/yum.repos.d/
* sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
* sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
* yum update -y
* sudo systemctl start docker
* References: https://techglimpse.com/failed-metadata-repo-appstream-centos-8/

## Install docker-compose
* Follow steps mentioned in (link)[https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04]

## Pull the docker images
* sudo docker pull panyogesh/agw_gateway_python_pmn_systems:firstcut
* sudo docker tag panyogesh/agw_gateway_python_pmn_systems:firstcut agw_gateway_python
* get the docker-compose.yml file from pmn-systems : pmn-systems/lte/gateway/docker/docker-compose.yml
  in home directory [~]

## Prepare for installation
* sudo mkdir -p /var/opt/magma/certs
* copy the rootCA.pem file in /var/opt/magma/certs
* sudo mkdir -p /var/opt/magma/configs
* copy the gatway.mconfig file from  pmn-systems/lte/gateway/config/gateway.mconfig
* sudo touch /etc/snowflake
* create .env file with following contents in home directory [~]
```
COMPOSE_PROJECT_NAME=agw
DOCKER_USERNAME=
DOCKER_PASSWORD=
DOCKER_REGISTRY=
IMAGE_VERSION=latest
OPTIONAL_ARCH_POSTFIX=

BUILD_CONTEXT=../../..

CONTROL_PROXY_PATH=/var/opt/magma/configs/control_proxy.yml

SNOWFLAKE_PATH=/etc/snowflake
CERTS_VOLUME=/var/opt/magma/certs
CONFIGS_OVERRIDE_VOLUME=/var/opt/magma/configs
CONFIGS_OVERRIDE_TMP_VOLUME=/var/opt/magma/tmp

LOG_DRIVER=journald
```  

## Update the hosts file
* Assuming the orc8r installaed in 192.168.60.1
  - 192.168.60.1 controller.magma.test
  - 192.168.60.1 bootstrapper-controller.magma.test  

## Execute docker-compse file
* sudo docker-compose up -d

## Check for status
* sudo docker ps
* sudo docker exec magmad show_gateway_info.py
* sudo docker exec magmad checkin_cli.py
