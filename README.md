On startup, the application automatically creates required database tables if they do not exist.


## APT Build dependencies (non-pip)
1. python3-pip
2. mysql-server (I am using linux-mint)
3. dbeaver-ce (FOSS db client gui)
4. Setup local db, by creating test db and giving my test user all access `GRANT ALL PRIVILEGES ON test1.* TO 'test'@'localhost';`
## Pip dependencies (should all be in requirements.txt)
1. mysql-connectior-python
