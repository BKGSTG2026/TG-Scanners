#!/bin/bash

# Used to determine if this OS is running Debian 20.04 LTS or newer which impacts telegraf install
LINUX_DISTRO=$ID
LINUX_DISTRO_MAJOR_OS_VERSION=$VERSION_ID

# -----------------------------
# Install telegraf
# -----------------------------

case $LINUX_DISTRO in
    "linuxmint")
        if [ ! "$LINUX_DISTRO_MAJOR_OS_VERSION" -gt "20" ]; then
            echo "Linux distro '$LINUX_DISTRO' with major OS version '$LINUX_DISTRO_MAJOR_OS_VERSION' is older than Debian 20.04 LTS - you must install telegrapf manually - exiting"
            exit 1
        fi
        ;;
    "debian")
        if [ ! "$LINUX_DISTRO_MAJOR_OS_VERSION" -gt "12" ]; then
            echo "Linux distro '$LINUX_DISTRO' with major OS version '$LINUX_DISTRO_MAJOR_OS_VERSION' is older than Debian 20.04 LTS - you must install telegrapf manually - exiting"
            exit 1
        fi
        ;;
    *)
        echo "ERROR: Linux distro '$LINUX_DISTRO' not supported - exiting now."
        exit 1
    ;;
esac

curl --silent --location -O https://repos.influxdata.com/influxdata-archive.key

gpg --show-keys --with-fingerprint --with-colons ./influxdata-archive.key 2>&1 \
| grep -q '^fpr:\+24C975CBA61A024EE1B631787C3D57159FC2F927:$' \
&& cat influxdata-archive.key \
| gpg --dearmor \
| sudo tee /etc/apt/keyrings/influxdata-archive.gpg > /dev/null \
&& echo 'deb [signed-by=/etc/apt/keyrings/influxdata-archive.gpg] https://repos.influxdata.com/debian stable main' \
| sudo tee /etc/apt/sources.list.d/influxdata.list

sudo apt-get update && sudo apt-get install telegraf