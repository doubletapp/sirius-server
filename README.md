# sirius-server


```
CREATE DATABASE sirius_psql;
\c sirius_psql;
CREATE EXTENSION postgis;
CREATE USER admin WITH password 'PWD';
GRANT ALL privileges ON DATABASE sirius_psql TO admin;
```

* зависимости
```
sudo apt-get install sudo postgresql postgresql-server-dev-9.5
sudo apt-get install python3-psycopg2
sudo apt-get install nginx
```