# Following are the details for installation

## Base Image
Ubuntu 22.04.2 LTS

## Docker Installation
sudo apt  install docker.io

## Docker Compose (in root directory)

- mkdir -p ~/.docker/cli-plugins/
- curl -SL https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
- chmod +x ~/.docker/cli-plugins/docker-compose

## Verify Installation
* sudo docker compose
```
vagrant@rad-exp:~/magma-general-utility/PytestDemo$ sudo docker compose version
Docker Compose version v2.3.3
```
