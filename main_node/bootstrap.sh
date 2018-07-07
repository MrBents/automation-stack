#!/bin/bash
export FLASK_APP=./backend/server.py
source $(pipenv --venv)/bin/activate
flask run
