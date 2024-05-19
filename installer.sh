#!/bin/bash

# Create virtual environment
python -m venv tmp-env

# Activate virtual environment
source tmp-env/bin/activate

# Install Flask and its dependencies
pip install -r requirements.txt

# Run Flask application
python -m flask run 