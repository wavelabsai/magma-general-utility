# Flask Handler for Bevo Subscriber APIs
## Instructions:
* Install flask
* Run the `flask_handler.py` in a separate terminal tab inside the VM or the place where AGW is running
```bash
pip install flask
python flask_handler.py
```
* By default the server runs on port 5000, which can be changed in `flask_handler.py` line number 94
```
94    app.run(debug=True, port=5000)
```
* The port and server IP needs to be configured as `IP` and `PORT` available at the end of `subsciberdb.yml` (leave unchanged if using default IP and port for flask)

* Add subscriber using the following command
```bash
docker exec -it magmad pmn_subscriber_cli.py add --mcc=001 --mnc=01 --imsi=001010000000001 --st=1 --sd=000001 --opc=A3782F73B17811F4043EE66EBFD62519 --auth_key=5E4AB35891375D2AEE812E67C309A629 --subs_ambr_ul="2000 Mbps" --subs_ambr_dl="1000 Mbps" --dnn_name=apn1 --dnn_ambr_ul="2000 Mbps" --dnn_ambr_dl="1000 Mbps" --qos_profile_5qi=9
```
* The logs will be printed in syslog or can be seen in subscriberdb container logs