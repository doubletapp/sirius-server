# sirius-server


```
UPDATE pg_database SET datistemplate = FALSE WHERE datname = 'template1';
DROP DATABASE Template1;
CREATE DATABASE sirius_psql3 OWNER kokokotlin ENCODING = 'UTF-8' lc_collate = 'en_US.utf8' lc_ctype = 'en_US.utf8' template template0;
\c sirius_psql3;
CREATE EXTENSION postgis;
CREATE USER kokokotlin WITH password 'PWD';
GRANT ALL privileges ON DATABASE sirius_psql3 TO kokokotlin;
SET client_encoding = 'UTF8';
```

# зависимости
```
sudo apt-get install sudo postgresql postgresql-server-dev-9.5 postgis
sudo apt-get install python3-psycopg2
sudo apt-get install nginx
```

# конфиги
```
sudo cp config/sirius-nginx.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/sirius-nginx.conf /etc/nginx/sites-enabled/sirius-nginx.conf
sudo service nginx reload
sudo service nginx restart

sudo cp config/gunicorn.service /etc/systemd/system/gunicorn.service
sudo cp config/gunicorn.conf /etc/init/gunicorn.conf
cp local_settings_example.py local_settings.py
```

# миграции и статитка
```
manage.py migrate
manage.py collectstatic

```

# запуск
`sudo service gunicorn start`