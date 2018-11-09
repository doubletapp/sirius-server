# sirius-server


```
CREATE DATABASE sirius_psql OWNER kokokotlin;
\c sirius_psql;
CREATE EXTENSION postgis;
CREATE USER kokokotlin WITH password 'PWD';
GRANT ALL privileges ON DATABASE sirius_psql TO kokokotlin;
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
```

# миграции и статитка
```
manage.py migrate
manage.py collectstatic

```

# запуск
`sudo service gunicorn start`