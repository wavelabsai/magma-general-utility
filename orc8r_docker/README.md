## Deploying the Orchestrators v1.8
#### The documentation is meant to help you deploy the Magma core orchestrators for testing, not for production 
##### Install Docker Engine (incl. Docker Compose)
```
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
##### Now create some directories that we will be using on this installationmkdir -p /magma
```
mkdir -p /magma/certs
mkdir -p /magma/postgres
mkdir -p /magma/magmalte
mkdir -p /magma/docker_ssl_proxy
sudo wget https://raw.githubusercontent.com/magma/magma/v1.8/orc8r/cloud/docker/fluentd/conf/fluent.conf -P /magma/fluentd/conf/
sudo wget https://raw.githubusercontent.com/magma/magma/v1.8/nms/docker/docker_ssl_proxy/proxy_ssl.conf -P /magma/docker_ssl_proxy
git clone https://github.com/magma/magma.git
cd magma
git checkout v1.8
sudo cp -R orc8r/cloud/docker/controller/ /magma/
sudo cp -R orc8r/cloud/docker/fluentd /magma/
sudo cp -R orc8r/cloud/docker/metrics-configs/ /magma/
sudo cp -R nms/api /magma/magmalte/
sudo cp -R nms/app /magma/magmalte/
sudo cp -R nms/config /magma/magmalte/
sudo cp -R nms/generated /magma/magmalte/
sudo cp -R nms/scripts /magma/magmalte/
sudo cp -R nms/server /magma/magmalte/
sudo cp -R nms/shared /magma/magmalte/
```
##### Next get this script, it will help to create some of the certificates needed
```
sudo wget https://raw.githubusercontent.com/edaspb/Magma-Orchastrator-in-a-Docker-Swarm/master/scripts/certs.sh
sudo chmod +x certs.sh
sudo ./certs.sh
sudo ls -lh /magma/certs/
```
###### Edit the script to adapt it to your own needs 
Then you have to create the certs for the SSL on the docker nginx reverse proxy 
```
sudo openssl req -new -x509 -nodes -out /magma/docker_ssl_proxy/cert.pem -keyout /magma/docker_ssl_proxy/key.pem -days 365
```
Then create the certificate for the fluentd service, remember to change "yourdomain" by your own domain. 
```
cd /magma/certs/
sudo openssl genrsa -out fluentd.key 2048
sudo openssl req -new -key fluentd.key -out fluentd.csr -subj "/C=NI/CN=fluentd."yourdomain".com"
sudo openssl x509 -req -in fluentd.csr -CA certifier.pem -CAkey certifier.key -CAcreateserial -out fluentd.pem -days 3650 -sha256
```
##### Deploying the containers 

Now start all the containers. Use the next docker-compose files as if you are just deploying for testing, for production you have to change the database username and password on the files at least. But this is meant to be used for tests. 
In this files the database username is db_user, database password is db_password and the database name are db_name. Change that config with your owns. 
  There are 3 files are to be changed docker-compose-controller.yml,docker-compose-nms.yml,docker-compose-metrics.yml
  Do docker compose -f docker-compose-controller.yml up -d, docker compose -f docker-compose-metrics.yml up -d. 
##### Create the certs for the NMS.  
For that you can enter to the controller container and create the admin certificate. To do that follow the command 
```
docker ps --format '{{.Names}}' # DISPLAYS CONTAINERS NAMES
docker exec -it magma-controller-1 bash # ENTER TO THE CONTAINER THIS SHOULD BE THE NAME IF THE COMPOSE FILES ARE IN /MAGMA/
#### FROM HERE THIS COMMANDS ARE TO CREATE THE CERTS####
envdir /var/opt/magma/envdir /var/opt/magma/bin/accessc add-admin -duration 3650 -cert /var/opt/magma/bin/admin_operator admin_operator
openssl pkcs12 -export -out /var/opt/magma/bin/admin_operator.pfx -inkey /var/opt/magma/bin/admin_operator.key.pem -in /var/opt/magma/bin/admin_operator.pem
## THIS WILL REQUEST A PASSWORD, YOU CAN SET UP A PASSWORD OR JUST PRESS ENTER TWICE.
#### ENDING CREATING THE CERTS ####
#### EXIT THE CONTAINER ####
exit
#### NOW COPY THE CERTS TO THE /magma/certs/ folder ####
sudo docker cp magma-controller-1:/var/opt/magma/bin/admin_operator.key.pem /magma/certs/admin_operator.key.pem
sudo docker cp magma-controller-1:/var/opt/magma/bin/admin_operator.pem /magma/certs/admin_operator.pem
sudo docker cp magma-controller-1:/var/opt/magma/bin/admin_operator.pfx /magma/certs/admin_operator.pfx
```
After this host machine,go to file
C:\Windows\System32\drivers\etc
and edit host file as follows:

ip address host.yourdomain.com yourdomain.com
After this 
you can access nms at
https://host.yourdomain.com/nms
