#!/bin/sh
set -e

. /etc/os-release
ARCH=$(dpkg --print-architecture)

case "$ID" in
	ubuntu|linuxmint)
		UBUNTU_VER=$(lsb_release -rs)
		REPO_URL="https://packages.microsoft.com/ubuntu/${UBUNTU_VER}/prod"
		;;
	debian)
		REPO_URL="https://packages.microsoft.com/debian/${VERSION_ID}/prod"
		;;
	*)
		echo "Unsupported distribution: $ID"
		exit 1
		;;
esac

echo "Using Microsoft repo: $REPO_URL"

curl -fsSL https://packages.microsoft.com/keys/microsoft.asc |
	gpg --dearmor |
	tee /usr/share/keyrings/microsoft-prod.gpg > /dev/null

echo "deb [arch=$ARCH signed-by=/usr/share/keyrings/microsoft-prod.gpg] \
$REPO_URL main" \
> /etc/apt/sources.list.d/microsoft-prod.list

apt update
ACCEPT_EULA=Y apt install -y msodbcsql18 unixodbc-dev

