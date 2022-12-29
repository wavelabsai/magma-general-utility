#!/bin/bash

#This script modifies the threshold values of the ARP Cache 

#The minimum number of entries to keep in the ARP cache
#The garbage collector will not run if there are fewer than
#this number of entries in the cache.
gc_thresh1=8192

#The soft maximum number of entries to keep in the ARP
#cache.  The garbage collector will allow the number of
#entries to exceed this for 5 seconds before collection
#will be performed.
gc_thresh2=32768

#The hard maximum number of entries to keep in the ARP
#cache.  The garbage collector will always run if there are
#more than this number of entries in the cache.
gc_thresh3=65536

echo "Configurations Added/Updated: "
#Append or Update gc_thresh1
if [[ `grep "net.ipv4.neigh.default.gc_thresh1[[:blank:]]*=" /etc/sysctl.conf | wc -l` -eq 0 ]]; then
    echo "net.ipv4.neigh.default.gc_thresh1 = $gc_thresh1" | sudo tee -a /etc/sysctl.conf
else
    sudo sed -i -r "s~^net.ipv4.neigh.default.gc_thresh1[[:blank:]]*=[[:blank:]]*[0-9]*$~net.ipv4.neigh.default.gc_thresh1 = ${gc_thresh1}~" /etc/sysctl.conf
    echo "net.ipv4.neigh.default.gc_thresh1 = $gc_thresh1"
fi

#Append or Update gc_thresh2
if [[ `grep "net.ipv4.neigh.default.gc_thresh2[[:blank:]]*=" /etc/sysctl.conf | wc -l` -eq 0 ]]; then
    echo "net.ipv4.neigh.default.gc_thresh2 = $gc_thresh2" | sudo tee -a /etc/sysctl.conf
else
    sudo sed -i -r "s~^net.ipv4.neigh.default.gc_thresh2[[:blank:]]*=[[:blank:]]*[0-9]*$~net.ipv4.neigh.default.gc_thresh2 = ${gc_thresh2}~" /etc/sysctl.conf
    echo "net.ipv4.neigh.default.gc_thresh2 = $gc_thresh2"
fi

#Append or Update gc_thresh3
if [[ `grep "net.ipv4.neigh.default.gc_thresh3[[:blank:]]*=" /etc/sysctl.conf | wc -l` -eq 0 ]]; then
    echo "net.ipv4.neigh.default.gc_thresh3 = $gc_thresh3" | sudo tee -a /etc/sysctl.conf
else
    sudo sed -i -r "s~^net.ipv4.neigh.default.gc_thresh3[[:blank:]]*=[[:blank:]]*[0-9]*$~net.ipv4.neigh.default.gc_thresh3 = ${gc_thresh3}~" /etc/sysctl.conf
    echo "net.ipv4.neigh.default.gc_thresh3 = $gc_thresh3"
fi

if [[ (`grep "net.ipv4.neigh.default.gc_thresh1[[:blank:]]*=[[:blank:]]*$gc_thresh1" /etc/sysctl.conf | wc -l` -eq 1 )
    && ( `grep "net.ipv4.neigh.default.gc_thresh2[[:blank:]]*=[[:blank:]]*$gc_thresh2" /etc/sysctl.conf | wc -l` -eq 1 )
    && ( `grep "net.ipv4.neigh.default.gc_thresh3[[:blank:]]*=[[:blank:]]*$gc_thresh3" /etc/sysctl.conf | wc -l` -eq 1 ) ]]; then
    logger "INFO: ARP Table Configurations added successfully"
else
    logger "ERROR: Failed to add ARP Table Configurations"
fi
