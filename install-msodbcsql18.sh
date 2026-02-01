#!/bin/sh
set -e

. /etc/os-release
ARCH=$(dpkg --print-architecture)
# Key and repo paths
KEYRING=/usr/share/keyrings/microsoft-prod.gpg
REPO_FILE=/etc/apt/sources.list.d/microsoft-prod.list

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

# Download Microsoft key if missing
if [ ! -f "$KEYRING" ]; then
    echo "Fetching Microsoft GPG key..."
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee "$KEYRING" > /dev/null
    sudo chmod 644 "$KEYRING"
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
echo "deb [arch=$ARCH signed-by=$KEYRING] $REPO_URL $SUITE main" | sudo tee "$REPO_FILE"

# Update apt and install packages
echo "Updating apt and installing MS ODBC driver..."
sudo apt update
sudo ACCEPT_EULA=Y apt install -y msodbcsql18 unixodbc-dev

echo "msodbcsql18 installed successfully"
