#!/bin/bash
source $(poetry env info --path)/bin/activate
export APP_MODULE='casepro.wsgi:application'
./django-entrypoint.sh