# Few improvments for tunining the performance

## ARP entries tuning

* Issue : The number of arp entries supported by default in linux is around 1000
          If more number of arp entries are added, retries are observed
* Solution : Run the attached arp script "arp-tuning.sh" and it will increase
             the supported arp entries to 8k
```bash
agrant@distro-magma:/var/core$ cat /etc/sysctl.conf  | grep "gc_thresh"
net.ipv4.neigh.default.gc_thresh1 = 8192
net.ipv4.neigh.default.gc_thresh2 = 32768
net.ipv4.neigh.default.gc_thresh3 = 65536
vagrant@distro-magma:/var/core$```

