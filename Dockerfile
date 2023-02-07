FROM python:3.9-slim-bullseye AS compile-image
ARG ENVIRONMENT=development

## update debian and install build deps
RUN apt-get update && apt-get install -y \
        gcc \
        libc-dev \
        python3-dev\
        default-libmysqlclient-dev \
        build-essential 
        #default-mysql-client 
        # libmysqlclient-dev \
        # linux-headers \
        #libjpeg-dev \
        # zlib1g-dev \
        # 
        # libmariadb3 \
        # libmariadb-dev
        #mariadb-client
        #postgresql-dev


## virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

## install requirements
RUN pip install --upgrade pip wheel pip-tools

COPY requirements.txt ./requirements.in

## update requirements file with deployment requirement deps
RUN echo "gunicorn" >> /requirements.in
RUN echo "mysqlclient" >> /requirements.in

RUN pip-compile ./requirements.in > ./requirements.txt  &&\
    pip-sync &&\
    pip install -r ./requirements.txt

FROM python:3.9-slim-bullseye AS runtime-image
ARG ENVIRONMENT=development

# partially inspired from https://github.com/tiangolo/meinheld-gunicorn-docker

## update alpine and install runtime deps
RUN apt-get update && apt-get install -y \
        # libjpeg-turbo \
        # zlib \
        # libjpeg \
        openssl \
        ca-certificates \
        #mariadb-connector-c \
        libmariadb3 \
        libmariadb-dev\
        nginx \
        python3-pip \
        python3-cffi \
        python3-brotli \
        libpango-1.0-0 \
        libpangoft2-1.0-0 \
        vim

## copy Python dependencies from build image
COPY --from=compile-image /opt/venv /opt/venv

## prepare nginx
COPY nginx.conf /etc/nginx/http.d/default.conf
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./app /app
WORKDIR /app/


ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Meinheld
CMD ["/start.sh"]
