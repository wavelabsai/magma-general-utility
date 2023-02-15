* Clone the repo
```bash
HOST $ git clone https://github.com/wavelabsai/magma-general-utility.git
HOST $ cd magma-general-utility/wldistro_deploy/feg-install
```
* Place the file ```rootCA.pem``` in ```magma-general-utility/wldistro_deploy/feg-install```,  and edit```control_proxy.yml```and ```.env```, if needed, present in the same directory:

>```rootCA.pem``` to be obtained from the ```Orc8r```

* Run the feg install script
```bash
vagrant@feg:~magma-general-utility/wldistro_deploy/feg-install$ sudo ./install_gateway.sh feg
```