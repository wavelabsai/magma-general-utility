# This is for internet connectvitiy issue

## Add IP-Table rules for Internet access
* iptables -t nat -A POSTROUTING -o eno2 -j SNAT --to 172.16.4.30

## Connecting to orchestrator
iptables -t nat -I PREROUTING --src 192.168.90.221 --dst 44.0.0.0/8  -j ACCEPT
iptables -t nat -I PREROUTING --src 192.168.90.221 --dst 34.0.0.0/8  -j ACCEPT
iptables -t nat -I PREROUTING --src 192.168.90.221 --dst 52.0.0.0/8  -j ACCEPT

## To delete the IPtables
iptables -t nat -D PREROUTING --src 192.168.90.221 --dst 44.0.0.0/8 -j ACCEPT
iptables -t nat -D PREROUTING --src 192.168.90.221 --dst 34.0.0.0/8 -j ACCEPT
iptables -t nat -D PREROUTING --src 192.168.90.221 --dst 52.0.0.0/8 -j ACCEPT

