#!/usr/bin/env bash

source .venv/bin/activate
FLASK_DEBUG=1 python -m flask run
deactivate
