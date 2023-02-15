## Provisioning the environment
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
## Installing FEG
* Navigate to the directory ```/opt/wldistro_deploy/feg-install```
```bash
vagrant@feg:$ cd /opt/wldistro_deploy/feg-install
```
* Place the file ```rootCA.pem``` in ```/opt/wldistro_deploy/feg-install```,  and edit```control_proxy.yml```and ```.env```, if needed, present in the same directory:

>```rootCA.pem``` to be obtained from the ```Orc8r```

* Run the feg install script
```bash
vagrant@feg:~/opt/wldistro_deploy/feg-install$ sudo ./install_gateway.sh feg
```