On startup, the application automatically creates required database tables if they do not exist.

## Running locally
1. Ensure dependencies are installed
2. Ensure mysql driver & mysql server are installed correctly
3. Ensure db credentials are correct for connecting to local mysqldb (by updating .env file) 
4. Run with `python3 -m tg_scanners.main --mode mock` from application root to run te service persistently and continuously send mock data. You can also run with `python3 -m tg_scanners.main --mode server` to connect to a TCP/Ip scanner instead. If running with the `--mode mock` argument, you should be able to connect to the table suing DBeaver and see the data streamed in.

## APT dependencies (non-pip)
1. python3-pip
2. mysql-server (I am using linux-mint)
3. dbeaver-ce (FOSS db client gui). Use to validate data is being sent correctly to db
4. Setup local db, by creating test db and giving my test user all access `GRANT ALL PRIVILEGES ON test1.* TO 'test'@'localhost';`

## Pip dependencies (should all be in requirements.txt)
1. pip install -r requirements.txt

## Setting up the Python Virtual Env (venv)
1. (On a raspberry pi) Install  python3-venv & pip with `sudo apt install -y python3-venv python3-pip`
2.  Setup `/opt` to run the application 
    ```
    $> sudo mkdir -p /opt/tg-scanners
    $> cd /opt/tg-scanners
    $> python3 -m venv venv
    $> sudo chown -R <user>:<user> /opt/tg-scanners # USER should be non-root user needed to run the application
    ```
3. Hop into the venv with `source venv/bin/activate` - you should see your prompt change
4. While still in the venv, install the pip dependencies as the service user `sudo -u <user> /opt/tg-scanners/venv/bin/pip install -r requirements.txt`

## Packaging
This repo contains an `makefile` which turns this python code into a `.deb` file that can be installed on any debain-based system. 
- `make clean`: Cleans out the `/dist` folder - should be done before running the packaging command
- `make package`: Creates the `.deb` file that can be used to install the python code, create the required users and installs the service file in the correct location
	- NOTE: If you are building this on a pi, you MUSt update the architechture to use 'arm64 by doing `make package ARCH=arm64``

## Build / Packaging dependencies
1. `sudo apt install -y ruby ruby-dev build-essential`
2. `sudo gem install --no-document fpm`
## Rapsberry Pi Setup

### QOL Things
1. Updates aliases for root

### Packages Installed
1. vim


### Setup
1. Clone the git repo
2. Run `make package`
	- If there is an error saying that you need to install fpm, then you need to install it along with ruby by `sudo apy install ruby; sudo gem install fpm. Then try the `make package` command again. If you see the message "DEB package created sueccessfully", and there is a file located in the local `dist` folder` thed the command executed successfully.
3. Install the package with `sudo apt install ./dist/tg-scanners_1.0.0_arm64.deb` (NOTE: the architechture may change based on where you are installing it - on a raspberry pi, it should have the 'arm' architechture'). If you are prompted to install a dependency. install it

