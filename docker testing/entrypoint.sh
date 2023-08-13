#!/bin/sh

set -ex

# Create virtual env, activate it and install PIL
pip install virtualenv
virtualenv docker-venv
source docker-venv/bin/activate
pip install -r requirements.txt

cp -f -r docker-venv/lib/python3.9/site-packages/ deployment/
cp -f main.py deployment/main.py

# Remove temp files
zip -r deployment
rm -rf docker-venv
rm -rf deployment
