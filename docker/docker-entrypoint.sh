#!/bin/sh

set -e

poetry run python3 main.py

exec "$@"
