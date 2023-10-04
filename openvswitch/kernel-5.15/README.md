# For bringing up OVS 2.15 for kernel version 5.15.0

## Openvswich
* version : 2.15
* Features : gtp
  
## Kernel 
* verion: 5.15

## Core Magma

## Procedure
* https://github.com/magma/magma/blob/master/third_party/gtp_ovs/ovs-gtp-patches/2.15/build.sh
  ```
  sudo apt update
  sudo apt install -y build-essential linux-headers-generic
  sudo apt install -y dh-make debhelper dh-python devscripts python3-dev
  sudo apt install -y graphviz libssl-dev python3-all python3-sphinx libunbound-dev libunwind-dev
  sudo apt-get install libelf-dev
  sudo apt-get install module-assistant

  export OVS_VER='2.15'
  export MAGMA_ROOT=/home/vagrant/magma/
  git clone  https://github.com/openvswitch/ovs
  cd ovs/
  git checkout 31288dc725be6bc8eaa4e8641ee28895c9d0fd7a
  git apply "$MAGMA_ROOT/third_party/gtp_ovs/ovs-gtp-patches/$OVS_VER"/00*
  patch -p1 < [link](https://github.com/wavelabsai/magma-general-utility/blob/master/openvswitch/kernel-5.15/Fix-OVS-kernel-5.15.diff)
  ```

 **NOTE**: For any broken dependencies use : sudo apt --fix-broken install
  
