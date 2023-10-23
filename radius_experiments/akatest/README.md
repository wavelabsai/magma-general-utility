# For configuratiaon of EAP-AKA using hostapd and eapol_test

## Docker Image
* Build: sudo docker build -t aka_exp:oct21 .
* Run  : sudo docker run -it --name radiusexperiments --security-opt apparmor=unconfined --cap-add CAP_SYS_ADMIN --cap-add=NET_ADMIN  --rm aka_exp:oct21 bash


## Topology
[Namespace:wiredns0]veth0 -------veth1[Namspace:wiredns1]

* Namepace:wiredns0 -> Binary: hlr_auc_gw, hostapd
* Namepace:wiredns1 -> Binary: eapol_test

## Configuation

### Creating Namespace:
```
sudo ip netns add wiredns0
sudo ip netns add wiredns1
sudo ip link add veth0 type veth peer name veth1

sudo ip link set veth0 netns wiredns0
sudo ip link set veth1 netns wiredns1
sudo ip netns exec wiredns0 ip addr add 30.0.0.1/24 dev veth0
sudo ip netns exec wiredns1 ip addr add 30.0.0.2/24 dev veth1
sudo ip netns exec wiredns0 ifconfig veth0 up
sudo ip netns exec wiredns1 ifconfig veth1 up
```

### TERMINAL-1
```
sudo docker run -it --name radiusexperiments --security-opt apparmor=unconfined --cap-add CAP_SYS_ADMIN --cap-add=NET_ADMIN  --rm aka_exp:oct21 bash
```

#### Running hlr_auc_gw
```
sudo docker exec -it radiusexperiments bash
/hostap/hostapd/hlr_auc_gw -u -m /var/configs/hlr_auc_gw.milenage_db
```

### TERMINAL-2
```
sudo docker exec -it radiusexperiments bash
/hostap/hostapd/hostapd /var/configs/eap_aka_hostapd.conf -dd
```

### TERMINAL-3
```
sudo docker exec -it radiusexperiments bash
/wpa_supplicant/wpa_supplicant/eapol_test -i veth1 -a30.0.0.1 -c /var/configs/eap_aka_wpa_supplicant.conf
```
