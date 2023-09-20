# Usage of CLIs

## strict_pmn_cli.py
- add
  ```
  python3.8 strict_pmn_cli.py add --mcc=001 --mnc=001 --imsi=IMSI001011234567522 --st=1 --sd=000001 --opc=A3782F73B17811F4043EE66EBFD62519 --auth_key=5E4AB35891375D2AEE812E67C309A629 --subs_ambr_ul="2000 Mbps" --subs_ambr_dl="1000 Mbps" --dnn_name=apn1 --dnn_ambr_ul="2000 Mbps" --dnn_ambr_dl="1000 Mbps" --qos_profile_5qi=9
  ```
- delete
  ```
  strict_pmn_cli.py delete --imsi=IMSI001011234567524
  ```
