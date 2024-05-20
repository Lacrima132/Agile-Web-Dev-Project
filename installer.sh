#!/bin/bash

# Create virtual environment
python3 -m venv tmp-env

# Activate virtual environment (Unix-based systems)
source tmp-env/bin/activate

# Install Flask and its dependencies
pip install -r requirements.txt

# Set and export Flask secret key
export FLASK_SECRET_KEY=$(openssl rand -hex 32)

# Run Flask application
python3 -m flask runwsl
