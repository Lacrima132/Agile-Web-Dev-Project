#!/bin/bash

# Create virtual environment
python3 -m venv tmp-env

# Activate virtual environment
source tmp-env/bin/activate

# Install Flask and its dependencies
pip install -r requirements.txt

set FLASK_SECRET_KEY=$(openssl rand -hex 32)

# Run Flask application
python -m flask run 