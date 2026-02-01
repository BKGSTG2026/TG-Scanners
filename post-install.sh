#!/bin/sh
set -e

# Create group and user if missing
getent group tg-scanner >/dev/null || groupadd --system tg-scanner
getent passwd tg-scanner >/dev/null || \
    useradd --system --gid tg-scanner --home-dir /var/opt/tg-scanners \
    --shell /sbin/nologin --comment "TG Scanners service account" tg-scanner

# Fix ownership of the Python code
chown -R tg-scanner:tg-scanner /var/opt/tg-scanners

# Create Python venv if missing
if [ ! -d /var/opt/tg-scanners/venv ]; then
    sudo -u tg-scanner python3 -m venv /var/opt/tg-scanners/venv
fi

# Install dependencies if requirements.txt exists
if [ -f /var/opt/tg-scanners/requirements.txt ]; then
    sudo -u tg-scanner /var/opt/tg-scanners/venv/bin/pip install -r /var/opt/tg-scanners/requirements.txt
fi

# Ensure /etc/tg-scanners exists
mkdir -p /etc/tg-scanners
# Deploy default env file if not already present
if [ ! -f /etc/tg-scanners/tg-scanners.env ]; then
    cp tg-scanners.env /etc/tg-scanners/tg-scanners.env
    chown root:root /etc/tg-scanners/tg-scanners.env
    chmod 640 /etc/tg-scanners/tg-scanners.env
fi

# Reload systemd and enable the service
systemctl daemon-reload
systemctl enable tg-scanners.service

