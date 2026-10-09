# phaistos

The project is using [uv](https://docs.astral.sh/uv) as package and project 
manager. So, to get started working you first need to [install uv](https://docs.astral.sh/uv/getting-started/installation/)
and then issue the following command : 

```commandline
uv sync --extra dev
```

or if you still need `pip` compatible env : 

```commandline
uv pip install -r pyproject.toml --extra dev 
```

## Dependencies

Make sure you have a running MySQL database. If not you could 
spawn one with docker like :

Create a docker volume :
```commandline
docker volume create mysql-data
```

Create a MySQL instance
```commandline
docker run \
    -e MYSQL_ROOT_USERNAME=root \
    -e MYSQL_ROOT_PASSWORD=root_password \
    -v mysql-data:/var/lib/mysql \
    --name mysql \
    --restart unless-stopped \
    -d \
    mysql:8.0
```

Once the database instance is up & running, connect as a `root`
user and create a database :

```sql
mysql> create database phaistos_db character set utf8;
```

and finally, create the db user

```sql
CREATE USER 'phaistos'@'%' IDENTIFIED WITH mysql_native_password BY 'phaistos';
GRANT ALL PRIVILEGES ON phaistos_db.* TO 'phaistos'@'%';
flush privileges;
```



## Docker Info

Create a Docker network for the app
```commandline
docker network create phaistos-net
```

Attach the running mysql container to the application's network (assume the mysql container is called `mysql`)

```commandline
docker network connect --alias mysql phaistos-net mysql
```
```commandline
docker build . -t dideira/phaistos-web:latest
```

```commandline
docker run --rm -it --name phaistos \
    -e DJANGO_SETTINGS_MODULE=phaistos.settings.staging \
    -e DB_NAME=phaistos_db \
    -e DB_USER=phaistos \
    -e DB_PASS=phaistos \
    -e DB_HOST=mysql \
    -e DB_PORT=3306 \
    -e VIRTUAL_HOST=phaistos-dev.dide.ira.net \
    --network phaistos-net \
    dideira/phaistos-web:latest
```

or for local development

```commandline
docker run --rm -it --name phaistos \
    -e DJANGO_SETTINGS_MODULE=phaistos.settings.docker-dev \
    -p 8000:80 \
    dideira/phaistos-web:latest
```

or daemonize it
```commandline
docker run --name phaistos \
    -e DJANGO_SETTINGS_MODULE=phaistos.settings.staging \
    -e DB_NAME=phaistos_db \
    -e DB_USER=phaistos \
    -e DB_PASS=phaistos \
    -e DB_HOST=mysql \
    -e DB_PORT=3306 \
    -e VIRTUAL_HOST=phaistos-dev.dide.ira.net \
    -d \
    --network phaistos-net \
    --restart unless-stopped \
    dideira/phaistos-web:latest
```

# Nginx Proxy

In case you need a nginx proxy, then you may

```commandline
docker network create nginx-proxy
```

```commandline
docker run -d -p 80:80 --restart unless-stopped \
    --name nginx-proxy \
    -v /var/run/docker.sock:/tmp/docker.sock:ro \
    --net nginx-proxy \
    jwilder/nginx-proxy
```

Don't forget to add the nginx-proxy container to the `phaistos-net` network
```commandline
docker network connect phaistos-net nginx-proxy
```