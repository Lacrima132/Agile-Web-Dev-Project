#!/bin/bash

# Create virtual environment

python3 -m venv tmp-env

# Activate virtual environment
source tmp-env/bin/activate

# Install Flask and its dependencies
pip install flask
pip install flask-login
pip install flask-sqlalchemy

# Run Flask application
python3 -m flask run --debug

#run file using ./setup_and_run.sh