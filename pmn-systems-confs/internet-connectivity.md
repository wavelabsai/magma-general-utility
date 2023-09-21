# For internet connectivity issue

## Forwarding Tables
* iptables -t nat -A POSTROUTING -o eno1 -j MASQUERADE
* iptables -A FORWARD -i eth0 -o eno1 -j ACCEPT
* iptables -A FORWARD -i  eno1 -j ACCEPT

## Connecting to orchestrator
* iptables -t nat -I PREROUTING --src 192.168.90.221 --dst 34.0.0.0/8  -j ACCEPT
* iptables -t nat -I PREROUTING --src 192.168.90.221 --dst 44.0.0.0/8  -j ACCEPT
* iptables -t nat -I PREROUTING --src 192.168.90.221 --dst 54.0.0.0/8  -j ACCEPT
* iptables -t nat -I PREROUTING --src 192.168.90.221 --dst 52.0.0.0/8  -j ACCEPT

## To delete the IPtables
* iptables -t nat -D PREROUTING --src 192.168.90.221 --dst 34.0.0.0/8  -j ACCEPT
* iptables -t nat -D PREROUTING --src 192.168.90.221 --dst 44.0.0.0/8 -j ACCEPT
* iptables -t nat -D PREROUTING --src 192.168.90.221 --dst 54.0.0.0/8 -j ACCEPT
* iptables -t nat -D PREROUTING --src 192.168.90.221 --dst 52.0.0.0/8 -j ACCEPT
* iptables -t nat -D POSTROUTING -o eno1 -j MASQUERADE
* iptables -D FORWARD -i eth0 -o eno1 -j ACCEPT
* iptables -D FORWARD -i  eno1 -j ACCEPT

