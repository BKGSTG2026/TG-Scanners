# TG-Scanners

TG-Scanners is a Python-based scanning service designed to run reliably on Linux systems (including Raspberry Pi) and connect to a Microsoft SQL Server database using ODBC. It is distributed as a Debian (`.deb`) package and is intended to run as a long-lived `systemd` service.

This document explains **what the project does**, **how it is installed**, **how it is configured**, and **how it is operated and troubleshot**.

---

## High-Level Architecture

* **Language:** Python 3
* **Runtime model:** systemd-managed service
* **Packaging:** `.deb` built with `fpm`
* **Database connectivity:** ODBC (FreeTDS / unixODBC) to Microsoft SQL Server
* **Virtual environment:** Dedicated Python `venv` under `/var/opt/tg-scanners`
* **Configuration:** Environment file in `/etc/tg_scanners/tg-scanners.env`

The service runs as a background daemon and is designed to start automatically on boot.

---

## System Requirements

### Operating System

* Debian-based Linux distribution

  * Raspberry Pi OS (64-bit recommended)
  * Ubuntu / Debian

* The python code should still work on Windows, it will just need some ajustments in engine.py

### Hardware

* Raspberry Pi (ARM64) or amd64 Linux host
* Network connectivity to the SQL Server

### Required Packages (handled automatically by the `.deb`)

* `python3`
* `python3-venv`
* `unixodbc`
* `unixodbc-dev`
* `freetds-bin`
* `freetds-dev`
* `tdsodbc`

You **do not** need to install these manually if you install via the installer.

---

## Installation

### 0. Build the `.deb` Package
From the root of the project, you will create the .deb (the installer) that is used to install the python code and configure it to run as a system service. 

From the project root, run:

```bash
make package
```

This should generate a `.deb` pacakge in the project's dist folder. You will use that file in the following steps. If you do not have the ability to 'make' the file, make sure make is installed by doing `sudo apt install make`

### 1. Install the `.deb` Package

From the project root (or wherever the package is located):

```bash
sudo apt install ./dist/tg-scanners_<version>_<arch>.deb
```

Example:

```bash
sudo apt install ./dist/tg-scanners_1.0.0_arm64.deb
```

Using `apt` (instead of `dpkg`) ensures all dependencies are automatically installed.

---

## What the Installer Does

During installation, the package performs the following actions:

1. Installs system dependencies via APT
2. Deploys application files to:

   ```
   /var/opt/tg-scanners
   ```
3. Creates a Python virtual environment:

   ```
   /var/opt/tg-scanners/venv
   ```
4. Installs Python dependencies from `requirements.txt`
5. Deploys the systemd service unit:

   ```
   /etc/systemd/system/tg-scanners.service
   ```
6. Creates the configuration directory:

   ```
   /etc/tg_scanners
   ```
7. Enables the service to start on boot

All of this logic lives in the package `post-install.sh` script.

---

## Configuration

### Environment File

TG-Scanners is configured via an environment file:

```bash
/etc/tg_scanners/tg-scanners.env
```

This file is **not overwritten on upgrades** and is intended for local, host-specific configuration.

Example:

```env
DB_HOST=sqlserver.example.com
DB_PORT=1433
DB_NAME=tg_scanners
DB_USER=scanner_user
DB_PASSWORD=supersecret
ODBC_DRIVER=FreeTDS
LOG_LEVEL=INFO
```

After editing this file, reload and restart the service

```bash
sudo systemctl daemon-reexec
sudo systemctl restart tg-scanners
```

---

## FreeTDS / ODBC Configuration

The service relies on FreeTDS for SQL Server connectivity.

### FreeTDS Configuration File

Installed or managed at:

```bash
/etc/freetds/freetds.conf
```

Ensure the contents of this local `freedts.conf` file are added to your system's `/etc/freetds/freetds.conf`
```

### ODBC Driver Registration

Ensure `tdsodbc` is registered in:

```bash
/etc/odbcinst.ini
```

Example:

```ini
[FreeTDS]
Description=FreeTDS ODBC Driver
Driver=/usr/lib/aarch64-linux-gnu/odbc/libtdsodbc.so
Setup=/usr/lib/aarch64-linux-gnu/odbc/libtdsS.so
```

---

## Service Management

### Service Name

```
tg-scanners.service
```

### Common Commands

Start the service:

```bash
sudo systemctl start tg-scanners
```

Stop the service:

```bash
sudo systemctl stop tg-scanners
```

Restart the service:

```bash
sudo systemctl restart tg-scanners
```

Check status:

```bash
sudo systemctl status tg-scanners
```

Enable on boot (this is done in the post-install script):

```bash
sudo systemctl enable tg-scanners
```

---

## Logs and Debugging

### systemd Logs

View logs:

```bash
journalctl -fu tg-scanners #view live logs
```

```bash
journalctl -eu tg-scanners #view all logs
```

### Common Issues

#### Service won’t start

* Check environment file syntax
* Verify database connectivity
* Ensure ODBC driver is installed

#### ODBC connection errors

* Confirm `freetds.conf` entries
* Validate driver path in `odbcinst.ini`
* Test with:

  ```bash
  tsql -H <host> -p 1433 -U <user>
  ```

---

## File Layout

```
# Code and python venv files
/var/opt/tg-scanners/
├── tg_scanners/
│   └── (python source)
├── venv/
│   └── bin/python
├── requirements.txt

# Environment variables
/etc/tg_scanners/
└── tg-scanners.env

# Systemd unit file
/etc/systemd/system/
└── tg-scanners.service
```

---

## Upgrades

To upgrade:

(TBD) But will probably be something like the following:

```bash
sudo apt install ./dist/tg-scanners_<newversion>_<arch>.deb
```

* Configuration files in `/etc/tg_scanners` are preserved
* The virtual environment may be updated if requirements change

---

## Uninstallation

```bash
sudo apt remove tg-scanners
```

Optional cleanup:

```bash
sudo rm -rf /var/opt/tg-scanners
sudo rm -rf /etc/tg_scanners
```

---

## Development Notes

* Packaging is handled via `Makefile` + `fpm`
* Dependencies are expressed as Debian package dependencies
* Python dependencies are installed at post-install time via the post-install.sh script

---

## Support

For issues:

* Check `journalctl` (as root) via `journalctl -eu tg-scanners` or `journalctl -fu tg-scanners` for live updates
* Validate ODBC connectivity independently
* Verify environment configuration

---

