


# Test and troubleshooting for Control Plane

## Additional Logging:

It is recommendable that before running the tests, enable some extra logging capabilities in Access Gateway to trace the call. For better details in Access Gateway logs:

-   Enable log_level: DEBUG in mme.yml, sessiond.yml and subscriberdb.yml
    
-   Enable print_grpc_payload: True on subscriberdb.yml, sessiond.yml & pipelined.yml
    
-   Restart magma, so the changes are taken
    
* See the logs using 
```bash
sudo journalctl -fu magma@mme or sudo journalctl -fu magma@subscriberdb or sudo journalctl -fu magma@sessiond
```
    

* Restart magma, so the changes are taken See the logs using 
```bash
sudo journalctl -fu magma@mme or sudo journalctl -fu magma@subscriberdb or sudo journalctl -fu magma@sessiond
```
  
  

### Common Issues and Troubleshooting:

#### SCTP Connection Failure

- **Description** :- NG Setup failure due to SCTP connection (like connection not established)
    
-   **Cause / Solution** :- One of the common cause for this the 5G Feature is not enabled properly from the swagger For checking the same
    
```bash
vagrant@magma-dev-focal:~/magma/lte/gateway$ cat /proc/net/sctp/eps
ENDPT SOCK STY SST HBKT LPORT UID INODE LADDRS
0 0 2 10 9 36412 0 465001933 192.168.60.142
0 0 2 10 25 38412 0 465001935 192.168.60.142
```
  #### UE Attach Failure

-   **Description** :- Ue is unable to attach to the network.
    
-   **Causes / Solution** :- Common causes for this failure is authentication failure. Please check the mme.log (/var/log/mme.log) to get the exact cause. In case of authentication failure, please verify that authentication parameters (such as key and opc) are the same in ue and subscriberdb.
    

#### During Traffic lost, please use below steps for initial phase of debugging 

1) Check magma services are up and running: 
```bash
service magma@* status.
```

For datapath health mme, sessions and pipelineD are important services to look at. Check syslog for ERRORs from services. If All looks good continue to next step.

2) Check for OVS services:

```bash
service openvswitch-switch status
```

3) Check OVS Bridge status: gtp ports might vary depending on number of eNB connected sessions. but ovs-vsctl show should not show any port with any errors. If you see GTP related error run /usr/local/bin/ovs-kmod-upgrade.sh. After running this command you need to reattach UEs.
```
ovs-vsctl show
```

4) Check if UE is actually connected to datapath using: 
```bash 
mobility_cli.py get_subscriber_table
```
 In case the IMSI is missing in this table, you need to debug issue in control plane. UE is not attached to the AGW, you need to inspect MME logs for control plane issues. If UE is connection continue to next step.

5) Please check the GTP traffic is rceived at enodeb interface or not using TCPdump.

6) Please check the table 0 entries in OVS flow:

```bash 
sudo ovs-ofctl -O OpenFlow13 dump-flows gtp_br0 table=0
```

7) Please check the table 13 entries in OVS flow:

```bash
sudo ovs-ofctl -O OpenFlow13 dump-flows gtp_br0 table=13
```

Above point-2 and point-3 should be increase the packet count and bytes in a uplink/downlink flows as respective traffic sending.

8) If above 3 points are OK then please check the NAT interface in pipelined.yml file.

9) If seen the packet count not increased in table 0 and/or table-13 then need to enable the debug level in OVS using below commands:

 ```bash
 sudo su
sudo ovs-appctl vlog/set netdev dbg
sudo ovs-appctl vlog/set ofproto dbg
sudo ovs-appctl vlog/set vswitchd dbg
sudo ovs-appctl vlog/set dpif dbg
echo 'module openvswitch +p' > /sys/kernel/debug/dynamic_debug/control
exit
sudo dmesg -n 7
sudo dmesg -C
```
After that execute the test case and collect logs using below command in console:
```bash
dmesg
```
---
### Test and troubleshooting for Control Plane

#### Additional Logging 

It is recommendable that before running the tests, enable some extra logging capabilities in Access Gateway to trace the call. 
For better details in Access Gateway logs:

-   Add parameter In `mme.yml`, `sessiond.yml` and `subscriberdb.yml`
```bash
log_level: DEBUG 
```
-   Add 
```bash
print_grpc_payload: True 
```
on `subscriberdb.yml`, `sessiond.yml` & `pipelined.yml`
    
-   Restart magma, so the changes are taken
    
-   See the logs using 
```bash
sudo journalctl -fu magma@mme or sudo journalctl -fu magma@subscriberdb or sudo journalctl -fu magma@sessiond
```

Restart magma, so the changes are taken See the logs using 
```bash
sudo journalctl -fu magma@mme or sudo journalctl -fu magma@subscriberdb or sudo journalctl -fu magma@sessiond
```
#### Common Issues and Troubleshooting:
**SCTP Connection Failure**

-   **Description** :- NG Setup failure due to SCTP connection (like connection not established)
    
-   **Cause / Solution** :- One of the common cause for this the 5G Feature is not enabled properly from the swagger For checking the same
    
```bash
vagrant@magma-dev-focal:~/magma/lte/gateway$ cat /proc/net/sctp/eps
ENDPT SOCK STY SST HBKT LPORT UID INODE LADDRS
0 0 2 10 9 36412 0 465001933 192.168.60.142
0 0 2 10 25 38412 0 465001935 192.168.60.142
```
 **UE Attach Failure**

-   **Description** :- Ue is unable to attach to the network.
    
-   **Causes / Solution** :- Common causes for this failure is authentication failure. Please check the mme.log (/var/log/mme.log) to get the exact cause. In case of authentication failure, please verify that authentication parameters (such as key and opc) are the same in ue and subscriberdb.
    
**During Traffic lost, please use below steps for initial phase of debugging:**

1) Check magma services are up and running: 
```bash
service magma@* status
```

For datapath health mme, sessions and pipelineD are important services to look at. Check syslog for ERRORs from services. If All looks good continue to next step.

2) Check for OVS services:

```bash
service openvswitch-switch status
```
3) Check OVS Bridge status: gtp ports might vary depending on number of eNB connected sessions. but ovs-vsctl show should not show any port with any errors. If you see GTP related error run `/usr/local/bin/ovs-kmod-upgrade.sh`
 After running this command you need to reattach UEs.
```bash
ovs-vsctl show
```

4) Check if UE is actually connected to datapath using: 
```bash
mobility_cli.py get_subscriber_table
```
 In case the IMSI is missing in this table, you need to debug issue in control plane. UE is not attached to the AGW, you need to inspect MME logs for control plane issues. If UE is connection continue to next step.

5) Please check the GTP traffic is rceived at enodeb interface or not using TCPdump.

6) Please check the table 0 entries in OVS flow:
```bash
sudo ovs-ofctl -O OpenFlow13 dump-flows gtp_br0 table=0
```
7) Please check the table 13 entries in OVS flow:

```bash
sudo ovs-ofctl -O OpenFlow13 dump-flows gtp_br0 table=13
```
Above point-2 and point-3 should be increase the packet count and bytes in a uplink/downlink flows as respective traffic sending.

8) If above 3 points are OK then please check the NAT interface in pipelined.yml file.

9) If seen the packet count not increased in table 0 and/or table-13 then need to enable the debug level in OVS using below commands:

  ```bash
  sudo su

sudo ovs-appctl vlog/set netdev dbg

sudo ovs-appctl vlog/set ofproto dbg

sudo ovs-appctl vlog/set vswitchd dbg

sudo ovs-appctl vlog/set dpif dbg

echo 'module openvswitch +p' > /sys/kernel/debug/dynamic_debug/control

exit

sudo dmesg -n 7

sudo dmesg -C
```

After that execute the test case and coland:

```bash
sudo su

sudo ovs-appctl vlog/set netdev info

sudo ovs-appctl vlog/set ofproto info

sudo ovs-appctl vlog/set vswitchd info

sudo ovs-appctl vlog/set dpif info

exit
```
To debug the traffic issues in fastpath, enable the OVS debug logging and check the logs using ```sudo dmesg```.

  
  Stop and start the `OVS Service` using below commands:

```sudo /usr/share/openvswitch/scripts/ovs-ctl stop```

```sudo /usr/share/openvswitch/scripts/ovs-ctl start```

In case of DL traffic, if you see datapath action, check if the dst ip address in tunnel() action is the right eNB for the UE.

-   Check routing table for this IP address `ip route get $dst_ip`
    
-   Check if the eNB is reachable from the AGW. there could be FW rules dropping the packets.
    

In case probe command shows drop you need to check which table is dropping the packet. Manually run the OVS trace command from above output shown on line starting with Running. For above DL example `sudo ovs-appctl ofproto/trace gtp_br0 tcp,in_port=local,ip_dst=192.168.128.12,ip_src=114.114.114.114,tcp_src=80,tcp_dst=3372`

**Intermittent packets Test and troubleshooting for Control Plane**

**Additional Logging:**

It is recommendable that before running the tests, enable some extra logging capabilities in Access Gateway to trace the call. For better details in Access Gateway logs:

-   Enable `log_level: DEBUG `in `mme.yml`, `sessiond.yml` and `subscriberdb.yml`
    
-   Enable `print_grpc_payload: True` on `subscriberdb.yml`, `sessiond.yml` & `pipelined.yml`
    
-   Restart magma, so the changes are taken
    
-   See the logs using 
```bash
 sudo journalctl -fu magma@mme or sudo journalctl -fu magma@subscriberdb or sudo journalctl -fu magma@sessiond
```
    

Restart magma, so the changes are taken See the logs using `sudo journalctl -fu magma@mme or sudo journalctl -fu magma@subscriberdb or sudo journalctl -fu magma@sessiond`

  
  

**Common Issues and Troubleshooting:**

**SCTP Connection Failure**

-   **Description** :- NG Setup failure due to SCTP connection (like connection not established)
    
-   **Cause / Solution** :- One of the common cause for this the 5G Feature is not enabled properly from the swagger For checking the same
    
```bash
vagrant@magma-dev-focal:~/magma/lte/gateway$ cat /proc/net/sctp/eps
ENDPT SOCK STY SST HBKT LPORT UID INODE LADDRS
0 0 2 10 9 36412 0 465001933 192.168.60.142
0 0 2 10 25 38412 0 465001935 192.168.60.142
```
 **UE Attach Failure**

-   **Description** :- Ue is unable to attach to the network.
    
-   **Causes / Solution** :- Common causes for this failure is authentication failure. Please check the mme.log (/var/log/mme.log) to get the exact cause. In case of authentication failure, please verify that authentication parameters (such as key and opc) are the same in ue and subscriberdb.
    

**During Traffic lost, please use below steps for initial phase of debugging:**

1) Check magma services are up and running: `service magma@* status`.

For datapath health mme, sessions and pipelineD are important services to look at. Check syslog for ERRORs from services. If All looks good continue to next step.

2) Check for OVS services:

`service openvswitch-switch status`

3) Check OVS Bridge status: gtp ports might vary depending on number of eNB connected sessions. but `ovs-vsctl` show should not show any port with any errors. If you see GTP related error run `/usr/local/bin/ovs-kmod-upgrade.sh`. After running this command you need to reattach UEs.

`ovs-vsctl show`

4) Check if UE is actually connected to datapath using: `mobility_cli.py get_subscriber_table`. In case the IMSI is missing in this table, you need to debug issue in control plane. UE is not attached to the AGW, you need to inspect MME logs for control plane issues. If UE is connection continue to next step.

5) Please check the GTP traffic is rceived at enodeb interface or not using TCPdump.

6) Please check the table 0 entries in OVS flow:

```bash
sudo ovs-ofctl -O OpenFlow13 dump-flows gtp_br0 table=0
```
7) Please check the table 13 entries in OVS flow:

```bash
sudo ovs-ofctl -O OpenFlow13 dump-flows gtp_br0 table=13
```
Above point-2 and point-3 should be increase the packet count and bytes in a uplink/downlink flows as respective traffic sending.

8) If above 3 points are OK then please check the NAT interface in pipelined.yml file.

9) If seen the packet count not increased in table 0 and/or table-13 then need to enable the debug level in OVS using below commands:

```bash
sudo su

sudo ovs-appctl vlog/set netdev dbg

sudo ovs-appctl vlog/set ofproto dbg

sudo ovs-appctl vlog/set vswitchd dbg

sudo ovs-appctl vlog/set dpif dbg

echo 'module openvswitch +p' > /sys/kernel/debug/dynamic_debug/control

exit

sudo dmesg -n 7

sudo dmesg -C
```
After that execute the test case and collect logs using below command in console:
```bash
dmesg
```
Disable the log level using below command:
```bash
sudo su

sudo ovs-appctl vlog/set netdev info

sudo ovs-appctl vlog/set ofproto info

sudo ovs-appctl vlog/set vswitchd info

sudo ovs-appctl vlog/set dpif info

exit
```
To debug the traffic issues in fastpath, enable the OVS debug logging and check the logs using ```sudo dmesg```.

  
  

Stop and start the `OVS Service` using below commands:

```sudo /usr/share/openvswitch/scripts/ovs-ctl stop```

```sudo /usr/share/openvswitch/scripts/ovs-ctl start```

In case of DL traffic, if you see datapath action, check if the dst ip address in tunnel() action is the right eNB for the UE.

-   Check routing table for this IP address ip route get $dst_ip
    
-   Check if the eNB is reachable from the AGW. there could be FW rules dropping the packets.
    

In case probe command shows drop you need to check which table is dropping the packet. Manually run the OVS trace command from above output shown on line starting with Running. For above DL example sudo ovs-appctl ofproto/trace gtp_br0 tcp,in_port=local,ip_dst=192.168.128.12,ip_src=114.114.114.114,tcp_src=80,tcp_dst=3372

**Intermittent packets drop:**

Intermittent packets loss is harder to debug than previous case. In this case the services and flow tables are configured currently but still some packets are dropped. Following are usual suspects:

1) TC queue is dropping packets due to rate limiting, command pipelined_cli.py debug qos shows stats for all dropped packets. Run the test case and observe if you see any dropped packets
```bash
root@agw:~# pipelined_cli.py debug qos

Root stats for: eth0

qdisc htb 1: root refcnt 2 r2q 10 default 0 direct_packets_stat 5487 ver 3.17 direct_qlen 1000 Sent 1082274 bytes 7036 pkt (dropped 846, overlimits 4244 requeues 0) backlog 0b 0p requeues 0

Root stats for: eth1
qdisc htb 1: root refcnt 2 r2q 10 default 0 direct_packets_stat 41140 ver 3.17 direct_qlen 1000 Sent 3603343 bytes 41337 pkt (dropped 0, overlimits 0 requeues 0) backlog 0b 0p requeues 0
```
2) NAT could be dropping packets. This can be due to no ports available in NAT table due to large number of open connections. AGW has default setting for the max connections sysctl net.netfilter.nf_conntrack_max and default range of source port sysctl net.ipv4.ip_local_port_range. If you see higher number of simultaneous connections, you need to tune these parameters.
