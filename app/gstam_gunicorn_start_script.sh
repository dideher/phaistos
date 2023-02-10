#!/bin/bash

export DJANGO_SETTINGS_MODULE="phaistos.settings.development"

python -m gunicorn -w 1 phaistos.wsgi
