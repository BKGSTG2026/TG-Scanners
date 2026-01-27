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