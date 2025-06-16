#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flask

# Create a database
touch database.db

# Initialize DB, make upload folder, seed database, and run Flask
flask init-db
mkdir -p static/uploads
python3 seed.py
flask run
