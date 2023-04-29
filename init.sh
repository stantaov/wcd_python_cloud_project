#!/bin/bash

# Install specific Python version to ensure a consistent environment across servers
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt install python3.8 -y
sudo apt install python3.8-distutils -y

# Install AWS CLI
sudo apt install awscli -y

# Create a virtual environment for Python 3.8
sudo apt install python3-virtualenv -y
virtualenv --python="/usr/bin/python3.8" sandbox
source sandbox/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

# Make run.sh executable
chmod a+x run.sh

# Create a log directory if it doesn't exist
mkdir -p log