#!/bin/bash
#
set -e

CWAG="cwag"
FEG="feg"

DIR="."
echo "Setting working directory as: $DIR"
cd "$DIR"

if [ -z $1 ]; then
  echo "Please supply a gateway type to install. Valid types are: ['$FEG', '$CWAG']"
  exit
fi

GW_TYPE=$1
echo "Setting gateway type as: '$GW_TYPE'"

if [ "$GW_TYPE" != "$FEG" ] && [ "$GW_TYPE" != "$CWAG" ]; then
  echo "Gateway type '$GW_TYPE' is not valid. Valid types are: ['$FEG', '$CWAG']"
  exit
fi

# Ensure necessary files are in place
if [ ! -f .env ]; then
    echo ".env file is missing! Please add this file to the directory that you are running this command and re-try."
    exit
fi

if [ ! -f rootCA.pem ]; then
    echo "rootCA.pem file is missing! Please add this file to the directory that you are running this command and re-try."
    exit
fi

# TODO: Remove this once .env is used for control_proxy
if [ ! -f control_proxy.yml ]; then
    echo "control_proxy.yml file is missing! Please add this file to the directory that you are running this command and re-try."
    exit
fi

source .env

#if [ "$GW_TYPE" == "$CWAG" ]; then
#  MODULE_DIR="cwf"
#
#  # Run CWAG ansible role to setup OVS
#  echo "Copying and running ansible..."
#  apt-add-repository -y ppa:ansible/ansible
#  apt-get update -y
#  apt-get -y install ansible
#  ANSIBLE_CONFIG="$INSTALL_DIR"/magma/"$MODULE_DIR"/gateway/ansible.cfg ansible-playbook "$INSTALL_DIR"/magma/"$MODULE_DIR"/gateway/deploy/cwag.yml -i "localhost," -c local -v -e ingress_port="${INGRESS_PORT:-eth1}" -e uplink_ports="${UPLINK_PORTS:-eth2 eth3}" -e li_port="${LI_PORT:-eth4}"
#fi

if [ "$GW_TYPE" == "$FEG" ]; then
  MODULE_DIR="$GW_TYPE"

  # Load kernel module necessary for docker SCTP support
  sudo tee -a /etc/modules <<< nf_conntrack_proto_sctp
fi

# Install Docker Engine (incl. Docker Compose)
sudo apt-get update
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    lsb-release \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Create snowflake to be mounted into containers
touch /etc/snowflake

echo "Placing configs in the appropriate place..."
mkdir -p /var/opt/magma
mkdir -p /var/opt/magma/configs
mkdir -p /var/opt/magma/certs
mkdir -p /etc/magma
mkdir -p /var/opt/magma/docker

# Copy default configs directory
cp -TR ./configs /etc/magma

# Copy config templates
cp -R ./configs/templates /etc/magma

# Copy certs
cp rootCA.pem /var/opt/magma/certs/

# Copy control_proxy override
cp control_proxy.yml /var/opt/magma/configs/

# Copy docker files
cp docker-compose.yml /var/opt/magma/docker/
cp .env /var/opt/magma/docker/

# Copy recreate_services scripts to complete auto-upgrades
cp recreate_services.sh /var/opt/magma/docker/
cp recreate_services_cron /etc/cron.d/

# Copy DPI docker files
#if [ "$GW_TYPE" == "$CWAG" ] && [ -f "$DPI_LICENSE_NAME" ]; then
#  MODULE_DIR="cwf"
#  mkdir -p "$SECRETS_VOLUME"
#  cp "$INSTALL_DIR"/magma/"$MODULE_DIR"/gateway/docker/docker-compose-dpi.override.yml /var/opt/magma/docker/
#  cp "$DPI_LICENSE_NAME" "$SECRETS_VOLUME"
#fi

cd /var/opt/magma/docker

if [ ! -z "$DOCKER_USERNAME" ] && [ ! -z "$DOCKER_PASSWORD" ] && [ ! -z "$DOCKER_REGISTRY" ]; then
 echo "Logging into docker registry at $DOCKER_REGISTRY"
 docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD" "$DOCKER_REGISTRY"
fi
docker compose --compatibility pull
docker compose --compatibility -f docker-compose.yml up -d

# Pull and Run DPI container
#if [ "$GW_TYPE" == "$CWAG" ] && [ -f "$DPI_LICENSE_NAME" ]; then
#  cd /var/opt/magma/docker
#  docker compose --compatibility -f docker-compose-dpi.override.yml pull
#  docker compose --compatibility -f docker-compose-dpi.override.yml up -d
#fi

echo "Installed successfully!!"
# Prepare rsyslog config and restart rsyslog
#echo "If you want syslog to be forwarded to the cloud execute following commands as well"
#echo "sudo cp $INSTALL_DIR/magma/orc8r/tools/ansible/roles/fluent_bit/files/60-fluent-bit.conf /etc/rsyslog.d/"
#echo "sudo service rsyslog restart"
