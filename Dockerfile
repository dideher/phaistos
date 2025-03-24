FROM python:3.9-slim-bullseye AS compile-image
ARG ENVIRONMENT=development
ARG DEBIAN_FRONTEND=noninteractive

RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		build-essential \
		pkg-config \
		default-libmysqlclient-dev \
		curl \
		ca-certificates \
	; \
	rm -rf /var/lib/apt/lists/*

## install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.24 /uv /bin/uv

# ## virtualenv
RUN uv venv --seed /opt/venv
# Use the virtual environment automatically
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

## install requirements
COPY pyproject.toml .
RUN uv pip install -r pyproject.toml --extra production --compile-bytecode

FROM python:3.9-slim-bullseye AS runtime-image
ARG ENVIRONMENT=development

# partially inspired from https://github.com/tiangolo/meinheld-gunicorn-docker

## update alpine and install runtime deps
RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
        openssl \
        ca-certificates \
        default-mysql-client \
        nginx \
        libpango-1.0-0 \
        libpangoft2-1.0-0 \
        vim \
	; \
	rm -rf /var/lib/apt/lists/*


## copy Python dependencies from build image
COPY --from=compile-image /opt/venv /opt/venv

## prepare nginx
COPY nginx.conf /etc/nginx/sites-available/default
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
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Meinheld
CMD ["/start.sh"]
