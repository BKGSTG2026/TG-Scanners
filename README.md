On startup, the application automatically creates required database tables if they do not exist.

## Running locally
1. Ensure dependencies are installed
2. Ensure mysql driver & mysql server are installed correctly
3. Ensure db credentials are correct for connecting to local mysqldb (by updating .env file) 
4. Run with `python3 -m tg_scanners.main` from application root

## APT dependencies (non-pip)
1. python3-pip
2. mysql-server (I am using linux-mint)
3. dbeaver-ce (FOSS db client gui)
4. Setup local db, by creating test db and giving my test user all access `GRANT ALL PRIVILEGES ON test1.* TO 'test'@'localhost';`
## Pip dependencies (should all be in requirements.txt)
1. pip install -r requirements.txt