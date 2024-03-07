# Steps for executing domain-proxy tests

## Prepare the env
* git clone https://github.com/magma/magma.git
* export MINIKUBE_DP_MAX_MEMORY=$(grep MemTotal /proc/meminfo | awk '{printf "%dm",$2/1024 - 1}')

## Install docker-compose
Ref: https://docs.docker.com/engine/install/ubuntu/
* for docker-compose
```
curl -SL https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

## Install HELM 
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

### Install the minikube 
```
curl -LO https://storage.googleapis.com/minikube/releases/v1.21.0/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```
### install kubectl
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

## Start the minikube
```
sudo usermod -aG docker $USER && newgrp docker
minikube start --memory=${MINIKUBE_DP_MAX_MEMORY} --addons=metrics-server --driver=docker --kubernetes-version=v1.20.7
```

## Execution

### Login to minikube
```
cd magma/dp
make _ci_init    (if make installed install make)
minikube ip
minikube ssh sudo ip link set docker0 promisc on
mkdir -p  /tmp/integration-tests-results
minikube mount  /tmp/integration-tests-results:/tmp/integration-tests-results &
```

### Install docker-compose in minikube
```
minikube ssh
curl -SL https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

## Run the tests
```
cd magma/dp
make _ci_integration_tests_orc8r
```



