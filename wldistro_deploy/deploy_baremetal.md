# Dockerized Deployment Guide (Baremetal)
Before proceeding further, follow through the `prerequisites.md`. This guide is for dockerized WLDistro `baremetal` deployment.
* Clone the repo
```bash
HOST $ git clone https://github.com/wavelabsai/magma-general-utility.git
HOST $ cd magma-general-utility/wldistro_deploy
```
* Change the name of the interface
```bash
HOST $ sudo su
ROOT $ sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="net.ifnames=0 biosdevname=0"/g' /etc/default/grub
ROOT $ sed -i 's/enp0s3/eth0/g' /etc/netplan/50-cloud-init.yaml
ROOT $ grub-mkconfig -o /boot/grub/grub.cfg
ROOT $ exit
```
* Reboot the Machine
```bash
HOST $ sudo reboot
```
* Copy the `rootCA.pem` file obtained from orchestrator into `/var/opt/magma/certs/`
```bash
HOST $ sudo mkdir -p /var/opt/magma/certs
HOST $ sudo vim /var/opt/magma/certs/rootCA.pem
```
* Execute the `agw_install_docker` script
```bash
HOST $ cd magma-general-utility/wldistro_deploy
HOST $ sudo bash ./agw_install_docker.sh
```
* Check whether the correct images are picked up
```bash
HOST $ cd /var/opt/magma/docker
HOST $ sudo docker image ls
```
* Check MME and PIPELINED
```bash
HOST $ sudo docker ps -a | grep -i pipe
HOST $ sudo docker ps -a | grep -i mme
```
* Check all the processes
```bash
HOST $ sudo docker ps -a
```
