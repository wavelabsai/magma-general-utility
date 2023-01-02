# Prerequisites

## Supported Operating Systems
Due to a number of dependencies on Ubuntu specific deployment and development tools, we've provided an Ubuntu specific guide
### Ubuntu

 1. Install the following Developer Tools
	 * [Docker](https://docs.docker.com/engine/install/ubuntu/) and [Docker Compose](https://docs.docker.com/compose/install/)
	 * [VirtualBox](https://www.virtualbox.org/wiki/Linux_Downloads)
	 * [Vagrant](https://www.vagrantup.com/downloads)

2. Install Golang Version 18
* Download the tar file
	```bash
	wget https://go.dev/dl/go1.18.3.linux-amd64.tar.gz
	```
* Extract the archive you downloaded into `/usr/local`, creating a Go tree in `/usr/local/go`.
*  Add  `/usr/local/go/bin`  to the PATH environment variable.
    ```bash
    export PATH=$PATH:/usr/local/go/bin
    ```
*  Verify that you've installed Go by opening a command prompt and typing the following command
    ```bash
    go version
	```
	You should expect something like this
    ```bash
    go version go1.18.3 linux/amd64
	```
3. Install `pyenv`
* Update system packages.
	```bash
	sudo apt update -y
	```
* Install some necessary dependencies.  **If you are using  `zsh`  instead of  `bash`, replace**  `.bashrc`  **for**  `.zshrc`.
	```bash
	apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev  libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
	```
	**Note**: For Ubuntu 22.04, use  `python3-openssl`  instead of  `python-openssl`.  
* Clone  `pyenv`  repository.
	```bash
	git clone https://github.com/pyenv/pyenv.git ~/.pyenv
	```
* Configure  `pyenv`.
	```bash
	echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
	echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
	echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -) "\nfi' >> ~/.bashrc
	exec "$SHELL"
	```
* Create python virtual environment version 3.8.10.
	```bash
	pyenv install 3.8.10
	pyenv global 3.8.10
	```
	**Note**: The  `pyenv`  installation  [might fail with a segmentation fault](https://github.com/pyenv/pyenv/issues/2046). Try using  `CFLAGS="-O2" pyenv install 3.8.10`  in that case.
* Install  `pip3`  and its dependencies.
	* Install  `pip3`.
		```bash
		sudo apt install python3-pip
		```
	* Install the following dependencies
	    ```bash
		pip3 install ansible fabric3 jsonpickle requests PyYAML
		```
* Install  `vagrant`  necessary plugin.
    ```bash
    vagrant plugin install vagrant-vbguest vagrant-disksize vagrant-reload
    ```
    Make sure  `virtualbox`  is the default provider for  `vagrant`  by adding the following line to your  `.bashrc`  (or equivalent) and restart your shell:  `export VAGRANT_DEFAULT_PROVIDER="virtualbox"`.
    
## Deployment Tooling
After following through the previous sections, install the following prerequisite tools.

1. [aws-iam-authenticator for Linux](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html).
2. [kubectl for Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-using-native-package-management).
3. [Helm for Linux](https://helm.sh/docs/intro/install/).
4. [Terraform for Linux](https://learn.hashicorp.com/tutorials/terraform/install-cli).
5. awscli
	```bash
	sudo apt install awscli
	```
### Orchestrator and NMS

Orchestrator deployment depends on the following components

1.  AWS account
2.  Registered domain for Orchestrator endpoints

We recommend deploying the Orchestrator cloud component of Magma into AWS. Our open-source Terraform scripts target an AWS deployment environment, but if you are familiar with devops and are willing to roll your own, Orchestrator can run on any public/private cloud with a Kubernetes cluster available to use. The deployment documentation will assume an AWS deployment environment - if this is your first time using or deploying Orchestrator, we recommend that you follow this guide before attempting to deploy it elsewhere.

Provide the access key ID and secret key for an administrator user in AWS (don't use the root user) when prompted by  `aws configure`. Skip this step if you will use something else for managing AWS credentials.

## Production Hardware

### Access Gateways

Access gateways (AGWs) can be deployed on to any AMD64 architecture machine which can support an Ubuntu 20.04 Linux installation. The basic system requirements for the AGW production hardware are

1.  2+ physical Ethernet interfaces
2.  AMD64 hexa-core processor around 2GHz clock speed or faster
3.  8GB RAM
4.  32GB or greater SSD storage

In addition, in order to build the AGW, you should have on hand

1.  A USB stick with 4GB+ capacity to load a  `Ubuntu 20.04.5 LTS (Focal Fossa) ` iso
2.  Peripherals (keyboard, screen) for your production AGW box for use during provisioning
