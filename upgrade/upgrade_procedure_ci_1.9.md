# Quick Start Guide for moving to 1.9 CI builds

This document contains the upgrade related steps from  `1.8` AGW to `CI 1.9 build`.

## Steps to be followed
* Check magma version before upgrade using the following command

```bash

apt list -i| grep magma

```

* Check the apt directory in 1.8 AGW Machine

  - Navigate to the directory `/etc/apt/sources.list.d/` add following line if not present :
     ```add-apt-repository 'deb https://linuxfoundation.jfrog.io/artifactory/magma-packages-test focal-ci main'```

     Keys can be added using the following command : 
     ```wget -qO - https://linuxfoundation.jfrog.io/artifactory/api/security/keypair/magmaci/public | apt-key add -``` 
 
    
* Stop and remove the magma services 

```bash
sudo service magma@* stop
sudo apt remove magma
sudo apt autoremove

```

* Install latest version of Magma from 1.9 CI Repository 

```bash
sudo apt-get update
sudo apt install magma
sudo apt install -y magma -o Dpkg::Options::="--force-overwrite"
```

 

* Ensure that the services are up and running 

```bash
sudo service magma@mme status
```

* Verify the Magma version post installations 
vagrant@test-magma:~$ apt list -i | grep magma
``` bash
  WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
  - libopenvswitch/focal-ci,now 2.15.4-10-magma amd64 [installed,automatic]
  - magma-cpp-redis/focal-ci,focal-ci,now 4.3.1.1-2 amd64 [installed,automatic]
  - magma-libfluid/focal-ci,now 0.1.0.7-1 amd64 [installed,automatic]
  - magma-libtacopie/focal-ci,focal-ci,now 3.2.0.1-1 amd64 [installed,automatic]
  - magma-sctpd/focal-ci,now 1.9.0-1671014871-ab406884 amd64 [installed,upgradable to: 1.9.0-1671145865-e2385452]
  - magma/focal-ci,now 1.9.0-1671014871-ab406884 amd64 [installed,upgradable to: 1.9.0-1671145865-e2385452]
  - openvswitch-common/focal-ci,now 2.15.4-10-magma amd64 [installed,automatic]
  - openvswitch-datapath-dkms/focal-ci,now 2.15.4-10-magma all [installed,automatic]
  - openvswitch-switch/focal-ci,now 2.15.4-10-magma amd64 [installed,automatic]
```

## COMMON ISSUES
