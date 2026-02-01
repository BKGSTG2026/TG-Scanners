#!/bin/sh
# Create system group if it doesn't exist
getent group tg-scanners >/dev/null || groupadd --system tg-scanners

# Create system user if it doesn't exist
getent passwd tg-scanners >/dev/null || \
    useradd --system --gid tg-scanners --home-dir /var/opt/tg-scanners --shell /sbin/nologin \
    --comment "TG Scanners service account" tg-scanners

