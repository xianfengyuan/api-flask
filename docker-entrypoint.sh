#!/bin/sh

flask db upgrade

exec gunicorp --bind 0.0.0.0:80 "app:create_app()"
