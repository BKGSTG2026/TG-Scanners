#!/bin/bash
set -euo pipefail

NAME=tg-scanners
VENV_DIR=/var/opt/$NAME/venv
ENV_FILE=/etc/$NAME/$NAME.env
PYTHON_BIN=python3

# Create system user if it doesn't exist
if ! id -u $NAME >/dev/null 2>&1; then
    useradd --system --home /var/opt/$NAME --shell /usr/sbin/nologin $NAME
fi

# Create venv
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_BIN -m venv $VENV_DIR
fi

# Activate venv and install dependencies
. $VENV_DIR/bin/activate
pip install --upgrade pip setuptools wheel
pip install pyodbc

# Detect architecture
ARCH=$(dpkg --print-architecture)

# Install ODBC drivers
if [ "$ARCH" = "amd64" ]; then
    # Install Microsoft ODBC driver for laptops / servers
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /usr/share/keyrings/microsoft-prod.gpg > /dev/null
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/ubuntu/22.04/prod jammy main" | sudo tee /etc/apt/sources.list.d/microsoft-prod.list
    sudo apt update
    sudo ACCEPT_EULA=Y apt install -y msodbcsql18 unixodbc-dev
#else
    # ARM / Raspberry Pi: install FreeTDS
    #sudo apt update
    #sudo apt install -y unixodbc unixodbc-dev freetds-bin freetds-dev tdsodbc
fi

# Configure DSN (example)
sudo mkdir -p /etc/odbcinst.ini.d
cat <<EOF | sudo tee /etc/odbcinst.ini
[$NAME]
Description = ODBC driver for $NAME
Driver = $(if [ "$ARCH" = "amd64" ]; then echo "/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.1.so.1.1"; else echo "/usr/lib/arm-linux-gnueabihf/odbc/libtdsodbc.so"; fi)
EOF

# Set permissions
sudo chown -R $NAME:$NAME /var/opt/$NAME
sudo mkdir -p /etc/$NAME
if [ ! -f "$ENV_FILE" ]; then
    sudo cp /var/opt/.env /etc/$NAME
    sudo chown $NAME:$NAME $ENV_FILE
fi

echo "Post-install complete!"

