# Dockerized Deployment Guide (Virtual Machine)
Before proceeding further, follow through the `prerequisites.md`. This guide is for dockerized WLDistro deployment in a Virtual Machine.
* Clone the repo
```bash
HOST $ git clone https://github.com/wavelabsai/magma-general-utility.git
```
*  Bring up the VM (use the bundeled `Vagrantfile`)
```bash
HOST $ cd magma-general-utility/wldistro_deploy
HOST $ vagrant up wldistro
```
* SSH into the VM
```bash
HOST $ vagrant ssh wldistro
```
* Perform following configurations
>1. Change the name of the interfaces on the VM
```bash
vagrant@WL-DISTRO-VM:~$ sudo su
root@WL-DISTRO-VM:/home/vagrant# sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="net.ifnames=0 biosdevname=0"/g' /etc/default/grub
root@WL-DISTRO-VM:/home/vagrant# sed -i 's/enp0s3/eth0/g' /etc/netplan/50-cloud-init.yaml
root@WL-DISTRO-VM:/home/vagrant# grub-mkconfig -o /boot/grub/grub.cfg
root@WL-DISTRO-VM:/home/vagrant# exit
vagrant@WL-DISTRO-VM:~$ exit
```
>2. Reload the machine
```bash
HOST $ vagrant reload wldistro
HOST $ vagrant ssh wldistro
```
>3. Login and check if the names are changed correctly to eth0, eth1, eth2
```bash
vagrant@WL-DISTRO-VM:~$ ip a
```
* Copy the `rootCA.pem` file obtained from orchestrator into `/var/opt/magma/certs/`
```bash
vagrant@WL-DISTRO-VM:~$ sudo mkdir -p /var/opt/magma/certs
vagrant@WL-DISTRO-VM:~$ sudo vim /var/opt/magma/certs/rootCA.pem
```
* Run the script that brings up the containers
```bash
vagrant@WL-DISTRO-VM:~$ cd /opt/wldistro_deploy/agw-install
vagrant@WL-DISTRO-VM:/opt/wldistro_deploy/agw-install$ sudo bash ./agw_install_docker.sh
```
* Check whether the correct images are picked up
```bash
vagrant@WL-DISTRO-VM:~$ cd /var/opt/magma/docker
vagrant@WL-DISTRO-VM:/var/opt/magma/docker$ sudo docker image ls
```
* Check MME and PIPELINED
```bash
vagrant@WL-DISTRO-VM:/var/opt/magma/docker$ sudo docker ps -a | grep -i pipe
vagrant@WL-DISTRO-VM:/var/opt/magma/docker$ sudo docker ps -a | grep -i mme
```
* Check all the processes
```bash
vagrant@WL-DISTRO-VM:/var/opt/magma/docker$ sudo docker ps -a
```
