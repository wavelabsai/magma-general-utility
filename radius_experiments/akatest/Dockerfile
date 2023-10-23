FROM ubuntu:22.04

RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install git libnl-3-dev libnl-genl-3-dev libssl-dev gcc libpcsclite-dev \
                    make libc6-dev libsqlite3-dev pkg-config libnl-route-3-dev binutils-dev \
                    libiberty-dev zlib1g-dev \
                    libdbus-1-dev libreadline-dev -y --no-install-recommends && \
    apt-get autoclean && \
    rm -rf /var/lib/dpkg/status-old /var/lib/apt/lists/*

RUN apt update
RUN apt install -y iproute2
RUN apt install -y net-tools

RUN git clone git://w1.fi/hostap.git  && cp hostap wpa_supplicant -R

RUN mkdir -p /var/configs/
ADD aka_config /var/configs/ 

#WORKDIR /hostap/hostapd/
WORKDIR /hostap/hostapd/
COPY  /hostap/tests/hwsim/example-hostapd.config /hostap/hostapd/.config 
RUN make
RUN make hlr_auc_gw

# wpa_supplicant
WORKDIR /wpa_supplicant/wpa_supplicant/

# Compare defconfig, if different, fail -> We may need to update our config (wpa_supplicant)
COPY /hostap/tests/hwsim/example-wpa_supplicant.config /wpa_supplicant/wpa_supplicant/.config
RUN make
RUN make eapol_test

CMD ["/bin/sh"]
