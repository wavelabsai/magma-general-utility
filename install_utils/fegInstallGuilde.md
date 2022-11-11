# Steps for Feg Installation

## Creation of Virtual Box (using vagrant)
* Open a terminal tab.
* Create a Vagrantfile
```bash
HOST $ vim Vagrantfile
```
>It should look something like this:
```bash
# -*- mode: ruby -*-  
# vi: set ft=ruby :  
  
Vagrant.configure("2") do |config|  
config.vm.box = "ubuntu/focal64"  
  
config.vm.define :feg, autostart: false do |feg|  
feg.vm.hostname = "feg"  
feg.vm.network "private_network", ip: "192.168.60.176", nic_type: "82540EM"  
feg.vm.network "private_network", ip: "192.168.129.74", nic_type: "82540EM"  
  
distromagma.vm.provider "virtualbox" do |vb|  
vb.name = "feg"  
vb.linked_clone = true  
vb.customize ["modifyvm", :id, "--memory", "6144"]  
vb.customize ["modifyvm", :id, "--cpus", "4"]  
vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]  
end  
end  
end
```
>*  Bring up the vm
```bash
HOST $ vagrant up feg
```
>* SSH into the vm
```bash
HOST $ vagrant ssh feg
```

## Installing FEG

* Clone the magma repo:

```bash
vagrant@feg:$ git clone -b v1.8 https://github.com/magma/magma.git
```
*Navigate to the directory ```magma/orc8r/tools/docker```
```bash
vagrant@feg:$ cd magma/orc8r/tools/docker
```
* Place the files ```rootCA.pem```, ```control_proxy.yml```, ```.env```  in the above directory:
>* ```rootCA.pem``` obtained from the ```Orc8r```
>*  ```control_proxy.yml``` for example:
```bash
vagrant@feg:~/magma/orc8r/tools/docker$ cat control_proxy.yml
# nghttpx config will be generated here and used
nghttpx_config_location: /var/tmp/nghttpx.conf

# Location for certs
rootca_cert: /var/opt/magma/certs/rootCA.pem
gateway_cert: /var/opt/magma/certs/gateway.crt
gateway_key: /var/opt/magma/certs/gateway.key

# Listening port of the proxy for local services. The port would be closed
# for the rest of the world.
local_port: 8443

# Cloud address for reaching out to the cloud.
cloud_address: controller.magma.test
cloud_port: 7443

bootstrap_address: bootstrapper-controller.magma.test
bootstrap_port: 7444

fluentd_address: fluentd.magma.test
fluentd_port: 24224

# Option to use nghttpx for proxying. If disabled, the individual
# services would establish the TLS connections themselves.
proxy_cloud_connections: True

# Allows http_proxy usage if the environment variable is present
allow_http_proxy: True
```

>* ```.env``` file for example:

```bash
vagrant@feg:~/magma/orc8r/tools/docker$ cat .env
COMPOSE_PROJECT_NAME=feg

DOCKER_REGISTRY=magmacore/
IMAGE_VERSION=1.8.0

GIT_HASH=v1.8

DOCKER_USERNAME=
DOCKER_PASSWORD=

ROOTCA_PATH=/var/opt/magma/certs/rootCA.pem
CONTROL_PROXY_PATH=/etc/magma/control_proxy.yml

SNOWFLAKE_PATH=/etc/snowflake
CONFIGS_DEFAULT_VOLUME=/etc/magma
CONFIGS_TEMPLATES_PATH=/etc/magma/templates

CERTS_VOLUME=/var/opt/magma/certs
CONFIGS_VOLUME=/var/opt/magma/configs

LOG_DRIVER=journald
```
* Run the feg install script
```bash
vagrant@feg:~/magma/orc8r/tools/docker$ sudo ./install_gateway.sh feg
```


## Output of FEG
```bash
vagrant@feg:~/magma/orc8r/tools/docker$ docker ps -a
CONTAINER ID   IMAGE                            COMMAND                  CREATED       STATUS                 PORTS     NAMES
9d972e6380bb   magmacore/gateway_go:1.8.0       "envdir /var/opt/mag…"   2 hours ago   Up 2 hours                       aaa_server
0ca7abd9971a   magmacore/gateway_python:1.8.0   "/bin/bash -c '/usr/…"   2 hours ago   Up 2 hours                       control_proxy
bd27e639ed79   magmacore/gateway_go:1.8.0       "envdir /var/opt/mag…"   2 hours ago   Up 2 hours                       health
597124f03f8d   magmacore/gateway_go:1.8.0       "envdir /var/opt/mag…"   2 hours ago   Up 2 hours                       session_proxy
461064b0d423   magmacore/gateway_python:1.8.0   "/bin/bash -c '/usr/…"   2 hours ago   Up 2 hours                       redis
11478fa79b14   magmacore/gateway_go:1.8.0       "envdir /var/opt/mag…"   2 hours ago   Up 2 hours                       eap_aka
b335feb94133   magmacore/gateway_go:1.8.0       "envdir /var/opt/mag…"   2 hours ago   Up 2 hours                       s8_proxy
358eb3aa4a8c   magmacore/gateway_go:1.8.0       "envdir /var/opt/mag…"   2 hours ago   Up 2 hours                       csfb
1ba5ba192937   magmacore/gateway_go:1.8.0       "envdir /var/opt/mag…"   2 hours ago   Up 2 hours                       swx_proxy
ae8a0b93f4b8   magmacore/gateway_python:1.8.0   "python3.8 -m magma.…"   2 hours ago   Up 2 hours                       eventd
26ddb87871f8   magmacore/gateway_python:1.8.0   "python3.8 -m magma.…"   2 hours ago   Up 2 hours                       magmad
340b06aea584   magmacore/gateway_go:1.8.0       "envdir /var/opt/mag…"   2 hours ago   Up 2 hours                       radiusd
4211da556e25   magmacore/gateway_go:1.8.0       "envdir /var/opt/mag…"   2 hours ago   Up 2 hours                       eap_sim
fead9515940a   magmacore/gateway_go:1.8.0       "envdir /var/opt/mag…"   2 hours ago   Up 2 hours                       feg_hello
cf221a408356   magmacore/gateway_go:1.8.0       "envdir /var/opt/mag…"   2 hours ago   Up 2 hours                       s6a_proxy
d114a33b3f01   magmacore/gateway_python:1.8.0   "/bin/bash -c '/usr/…"   2 hours ago   Up 2 hours (healthy)             td-agent-bit
```
## Common issues
* `checkin_cli.py` fails in locating `gateway.crt`
```bash
vagrant@feg:~/var/opt/magma/docker$ sudo docker exec -it magmad /usr/local/bin/checkin_cli.py
1. -- Testing TCP connection to controller.magma.test:7443 -- 
2. -- Testing Certificate -- 

> Error: [Errno 2] No such file or directory: '/var/opt/magma/certs/gateway.crt'

Suggestions
-----------
- Regenerate session certs
    1. Delete gateway.key and gateway.crt in /var/opt/magma/certs
    2. Restart magmad (sudo service magma@magmad restart)
- Ensure gateway has been registered in the cloud, with correct
  hardware ID and key
    1. Run show_gateway_info.py.
    2. Go to cloud swagger
        - E.g. https://127.0.0.1:9443/swagger/v1/ui/
        - Query the list gateways endpoint
    3. POST to add a new gateway, filling JSON with corresponding
       values from step 1.
```
> * A possible culprit might be missing/incorrect configurations in `/etc/hosts`
> * `/etc/hosts` must have entries for `controller`, `bootstrapper` and `fluentd`
> * For example:
```bash
vagrant@feg:~/magma/orc8r/tools/docker$ grep -e controller -e bootstrapper -e fluentd /etc/hosts
10.0.2.2 controller.magma.test
10.0.2.2 bootstrapper-controller.magma.test
10.0.2.2 fluentd.magma.test
```
> * Likewise, entries should be configured in `control_proxy.yml`
> * In conjuntion with the above example
```bash
vagrant@feg:~/magma/orc8r/tools/docker$ cat /var/opt/magma/configs/control_proxy.yml
                .
                .
                .
cloud_address: controller.magma.test
cloud_port: 7443
bootstrap_address: bootstrapper-controller.magma.test
bootstrap_port: 7444
fluentd_address: fluentd.magma.test
fluentd_port: 24224
                .
                .
                .
```
