# Fetch Subscribers Associated With a List of Networks from ORC8R
## Usage

```bash
mj@mjwl:~/tasks/orc8r/pmn-systems$ python3 subscriber_fetch_utility.py -h
usage: subscriber_fetch_utility.py [-h] Verbosity Key Cert Domain NetworksList [NetworksList ...]

List all the subscribers associated with a network

positional arguments:
  Verbosity     enter 'true' or 'false' to toggle verbose output
  Key           path to admin_operator.key.pem
  Cert          path to admin_operator.pem
  Domain        orc8r domain name or IP address
  NetworksList  a list of networks separated by spaces

options:
  -h, --help    show this help message and exit
```
## Example
* Non-verbose output
```bash
vagrant@orc8r:~/pmn-systems$ python3 subscriber_fetch_utility.py false .cache/test_certs/admin_operator.key.pem .cache/test_certs/admin_operator.pem magma.test test test2
```
---
```json
Network Name: test
[
   "IMSI001010000000002",
   "IMSI001010000000001"
]
Network Name: test2
[
   "IMSI901700000000001",
   "IMSI901700000000002"
]
```
* Verbose output
```bash
vagrant@orc8r:~/pmn-systems$ python3 subscriber_fetch_utility.py true .cache/test_certs/admin_operator.key.pem .cache/test_certs/admin_operator.pem magma.test test test2
```
---
```json
Network Name: test
{
   "IMSI001010000000001": {
      "active_apns": [
         "internet"
      ],
      "config": {
         "lte": {
            "auth_algo": "MILENAGE",
            "auth_key": "Rltc6LGZtJ+qXwou4jimvA==",
            "auth_opc": "6O0oneupUuQoO1TojmGDyg==",
            "state": "ACTIVE",
            "sub_profile": "default"
         }
      },
      "id": "IMSI001010000000001",
      "lte": {
         "auth_algo": "MILENAGE",
         "auth_key": "Rltc6LGZtJ+qXwou4jimvA==",
         "auth_opc": "6O0oneupUuQoO1TojmGDyg==",
         "state": "ACTIVE",
         "sub_profile": "default"
      },
      "name": "sub1"
   },
   "IMSI001010000000002": {
      "active_apns": [
         "internet"
      ],
      "config": {
         "lte": {
            "auth_algo": "MILENAGE",
            "auth_key": "Rltc6LGZtJ+qXwou4jimvA==",
            "auth_opc": "6O0oneupUuQoO1TojmGDyg==",
            "state": "ACTIVE",
            "sub_profile": "default"
         }
      },
      "id": "IMSI001010000000002",
      "lte": {
         "auth_algo": "MILENAGE",
         "auth_key": "Rltc6LGZtJ+qXwou4jimvA==",
         "auth_opc": "6O0oneupUuQoO1TojmGDyg==",
         "state": "ACTIVE",
         "sub_profile": "default"
      },
      "name": "sub2"
   }
}
Network Name: test2
{
   "IMSI901700000000001": {
      "config": {
         "lte": {
            "auth_algo": "MILENAGE",
            "auth_key": "AAECAwQFBgcICQoLDA0ODw==",
            "auth_opc": "AAECAwQFBgcICQoLDA0ODw==",
            "state": "ACTIVE",
            "sub_profile": "default"
         }
      },
      "id": "IMSI901700000000001",
      "lte": {
         "auth_algo": "MILENAGE",
         "auth_key": "AAECAwQFBgcICQoLDA0ODw==",
         "auth_opc": "AAECAwQFBgcICQoLDA0ODw==",
         "state": "ACTIVE",
         "sub_profile": "default"
      },
      "name": "z1"
   },
   "IMSI901700000000002": {
      "config": {
         "lte": {
            "auth_algo": "MILENAGE",
            "auth_key": "AAECAwQFBgcICQoLDA0ODw==",
            "auth_opc": "AAECAwQFBgcICQoLDA0ODw==",
            "state": "ACTIVE",
            "sub_profile": "default"
         }
      },
      "id": "IMSI901700000000002",
      "lte": {
         "auth_algo": "MILENAGE",
         "auth_key": "AAECAwQFBgcICQoLDA0ODw==",
         "auth_opc": "AAECAwQFBgcICQoLDA0ODw==",
         "state": "ACTIVE",
         "sub_profile": "default"
      },
      "name": "z2"
   }
}
```
**NOTE**: 
> * `admin_operator.pem` and `admin_operator.key.pem` to be obtained from `orc8r`
> * `domain` to be set as the `orc8r` domain for example `magma.test` as in the example above or `localhost` for local orc8r deployments, in case the script is also run locally