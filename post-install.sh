#!/bin/bash

# -----------------------------
# GLobal Variables 
# -----------------------------

# Get OS information
. /etc/os-release

APP_NAME=tg-scanners 
SERVICE_USER=tg-scanner

# Defines the python virtual environment that this uses to run
VENV_DIR=/var/opt/$APP_NAME/venv

# File that systemd uses for environment values for the python server and telegraf
PYTHON_SERVER_ENV_FILE=/etc/$APP_NAME/$APP_NAME.env
TELEGRAF_ENV_FILE=/etc/telegraf/telegraf.conf
FREETDS_ENV_FILE=/etc/freetds/freedts.conf

# Where the .deb installer puts the python server's systemd unit file
SERVICE_FILE_SRC=/var/opt/$APP_NAME/$APP_NAME.service

# Where the .deb installer puts the env/configration files
PYTHON_SERVER_ENV_FILE_SRC=/var/opt/$APP_NAME/.env
TELEGRAF_ENV_FILE_SRC=/var/opt/$APP_NAME/telegraf.conf
FREETDS_ENV_FILE_SRC=/var/opt/$APP_NAME/freetds.conf
PYTHON_BIN=python3

# System architecture
ARCH=$(dpkg --print-architecture)

# Check to see if telegraf is installed - if not, bail on installation and give the user instructions
if ! dpkg -s package_name >/dev/null ; then
    echo "ERROR: telegraf not installed! \
    Run `sudo ./var/opt/install-telegraf.sh` to install it and then try this installation again"
    exit 1
fi

# -----------------------------
# Directory & User creation
# -----------------------------

# Directories and their purposes:
# /var/opt/tg-scanners:
#   This is where the python server is deployed and runs out of (via the virtual environment)
#
# /etc/tg-scanners: This is were the .env file is installed and where the systemd service loads the env values for the python server
#
# /etc/telegraf: This contains the telegraf.conf file which contains the configuration details for telegraf

# Create system user if they doesn't exist - this is who systemd uses to run the python server
if ! id -u $SERVICE_USER >/dev/null 2>&1; then
    useradd --system --home /var/opt/$SERVICE_USER --shell /usr/sbin/nologin $SERVICE_USER
fi

# Make the app's system user the owner of the files
sudo chown -R $SERVICE_USER:$SERVICE_USER /var/opt/$APP_NAME

# Create the direcotry for the python server's environment values
sudo mkdir -p /etc/$APP_NAME

# If the python service file doesn't exist at /etc..., then copy it there
if [ ! -f "$PYTHON_SERVER_ENV_FILE" ]; then
    sudo cp $PYTHON_SERVER_ENV_FILE_SRC $PYTHON_SERVER_ENV_FILE
    sudo chown $SERVICE_USER:$SERVICE_USER $ENV_FILE
fi

# If the freetds config doesn't exist yet, add it
if grep -q "sqlserver" $FREETDS_ENV_FILE; then
    echo "No freetds config found, adding this local config"
    cat $FREETDS_ENV_FILE_SRC >> $FREETDS_ENV_FILE
fi

# add in telegraf config
cp $TELEGRAF_ENV_FILE_SRC $TELEGRAF_ENV_FILE

#todo remove this
# make storage directory if not exists
# sudo mkdir -p /var/lib/scanner
# sudo chown telegraf:telegraf /var/lib/scanner

# Create venv
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_BIN -m venv $VENV_DIR
fi

# Activate  python virtul environment
. $VENV_DIR/bin/activate

# Install python server dependencies in virtual environment, not at the system level
pip install --upgrade pip setuptools wheel
pip install  -r /var/opt/$APP_NAME/requirements.txt
pip install pyodbc
deactivate #  python virtual environment setup complete - exit it

# -----------------------------
# Configure DSN
# -----------------------------

# Configure DSN (testing)
# sudo mkdir -p /etc/odbcinst.ini.d
# cat <<EOF | sudo tee /etc/odbcinst.ini
# [$APP_NAME]
# Description = ODBC driver for $APP_NAME
# Driver = $(if [ "$ARCH" = "amd64" ]; then echo "/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.1.so.1.1"; else echo "/usr/lib/arm-linux-gnueabihf/odbc/libtdsodbc.so"; fi)
# EOF




# -----------------------------
# Deploy systemd unit files
# -----------------------------
cp $SERVICE_FILE_SRC /etc/systemd/system
chmod 640 /etc/systemd/system

# -----------------------------
# Start Services
# -----------------------------
systemctl daemon-reload
systemctl enable ${APP_NAME}.service --now
systemctl enable telegraf --now

echo "\nPost-install complete!"

# -----------------------------
# Checking service status
# -----------------------------
echo "Status of service '$APP_NAME' (python server): $(systemctl is-active $APP_NAME)"
if ! systemctl -q is-active $APP_NAME; then
    echo "ERROR: $APP_NAME is not started - use 'journalctl -eu $APP_NAME' to troubleshoot \
    and try restarting the service with 'sudo systemctl restart $APP_NAME" 
fi

echo "Status of service 'telegraf' (scanner listener): $(systemctl is-active telegraf)"
if ! systemctl -q is-active telegraf; then
    echo "ERROR: telegraf is not started - use 'journalctl -eu $APP_NAME' to troubleshoot \
    and try restarting the service with 'sudo systemctl restart telegraf" 
fi