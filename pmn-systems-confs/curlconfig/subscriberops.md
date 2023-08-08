## Steps to get the Curl Connected with OMS

* P9 -> OMS execute following commands.
```
import json
import requests
import urllib3
request_json={"am1.json":{"gpsis":["msisdn-001011234567534"],"internalGroupIds":["abcd1234-567-89-abcd"],"nssai":{"defaultSingleNssais":[{"sd":"000001","sst":1}],"singleNssais":[{"sd":"000002","sst":2},{"sd":"000003","sst":3}]},"subscribedUeAmbr":{"downlink":"2000 Mbps","uplink":"1000 Mbps"},"subscribedDnnList":["apn3"],"forbiddenAreas":[{"tacs":["000069"]}],"serviceAreaRestriction":{"restrictionType":"ALLOWED_AREAS","areas":[{"tacs":["000065","000066","000067"]}],"maxNumOfTAs":3},"plmnAmData":{"001-01":{}},"rfspIndex":7,"subsRegTimer":55,"ueUsageType":7,"micoAllowed":False}}

session = requests.Session()
session.verify = False
resp=requests.post('http://192.168.90.20:18080/oms-service/webapi/apiservice/ue_provision/ue_config/ue_config?rowData=%7B%20%20%22supi%22%3A%20%22001011234567534%22%7D', data=request_json, headers={"Content-Type": "multipart/form-data", "accept": "application/json", "apiInvokerId": "8meZD"})
```

## Steps to get the Curl Connected with UDR

### Get the UDR provision services
* kubectl get services --sort-by=.metadata.name --namespace intel-cil1-appln-udr-udr1

  ```udr-provision   ClusterIP   192.102.200.165   <none>        3000/TCP   9d```

### POST the request
* curl -v -X PUT -T am1.json http://192.102.200.165:3000/nudr-sp/v1/subs-724990000000009/5gs/imsi-724990000000009/subscription-data/provisioned-data/am-data -H "content-type:application/json"
* curl -v -X GET  http://192.102.200.165:3000/nudr-sp/v1/subs-724990000000009/5gs/imsi-724990000000009/subscription-data/provisioned-data/am-data -H "content-type:application/json"
* curl -v -X DELETE  http://192.102.200.165:3000/nudr-sp/v1/subs-724990000000009/5gs/imsi-724990000000009/subscription-data/provisioned-data/am-data -H "content-type:application/json"

### Sample Pods for UDR Provisioning
```
[root@on-prem cetnos]# kubectl get services --sort-by=.metadata.name --namespace intel-cil1-appln-udr-udr1 <<< Namespace of UDR
NAME            TYPE        CLUSTER-IP        EXTERNAL-IP   PORT(S)    AGE
udr-app         ClusterIP   192.102.98.213    <none>        3000/TCP   9d
udr-exp         ClusterIP   192.102.241.0     <none>        3000/TCP   9d
udr-notify      ClusterIP   192.102.146.85    <none>        8098/TCP   9d
udr-policy      ClusterIP   192.102.94.186    <none>        3000/TCP   9d
udr-polling     ClusterIP   192.102.100.144   <none>        8090/TCP   9d
udr-provision   ClusterIP   192.102.200.165   <none>        3000/TCP   9d
udr-subs        ClusterIP   192.102.155.69    <none>        3000/TCP   9d
udr-util        ClusterIP   192.102.182.152   <none>        8098/TCP   9d
[root@on-prem cetnos]#
```
