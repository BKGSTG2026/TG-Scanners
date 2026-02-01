#!/bin/sh
set -e

. /etc/os-release
ARCH=$(dpkg --print-architecture)

if [ -n "$VERSION_CODENAME" ]; then
	SUITE="$VERSION_CODENAME"
elif command -v lsb_release >/dev/null 2>&1; then
	SUITE="$(lsb_release -cs)"
else
	echo "Cannot determine Debian codename"
	exit 1
fi

if dpkg -s msodbcsql18 >/dev/null 2>&1; then
	echo "msodbcsql18 already installed"
	exit 0
fi

case "$ID" in
	ubuntu|linuxmint)
		SUITE="$(lsb_release -cs)"  # jammy, noble, etc
		REPO_URL="https://packages.microsoft.com/ubuntu/${UBUNTU_VER}/prod"
		;;
	debian)
		REPO_URL="https://packages.microsoft.com/debian/${VERSION_ID}/prod"
		SUITE="$VERSION_CODENAME" # bookworm, trixie, etc
		;;
	*)
		echo "Unsupported distribution: $ID"
		exit 1
		;;
esac

echo "Using Microsoft repo: $REPO_URL ($SUITE)"

curl -fsSL https://packages.microsoft.com/keys/microsoft.asc |
	gpg --dearmor |
	tee /usr/share/keyrings/microsoft-prod.gpg > /dev/null

echo "deb [arch=$ARCH signed-by=/usr/share/keyrings/microsoft-prod.gpg] \
$REPO_URL $SUITE main" \
> /etc/apt/sources.list.d/microsoft-prod.list

apt update
ACCEPT_EULA=Y apt install -y msodbcsql18 unixodbc-dev

