#!/usr/bin/env bash

cd ~/
PROJECT_DIR="$HOME/prgms/Python/jumpack-01"

# Create a project directory
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Create a virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Now install the libraries
pip install --upgrade pip
pip install --upgrade adafruit-circuitpython-ina228
pip install --upgrade RPi.GPIO
pip install --upgrade matplotlib

# Record the present state of the venv
PKG_LIST="requirements.txt" > "./docs/$PKG_LIST"         # clobber the old file
echo -e "# file: ${PKG_LIST}" >> "./docs/${PKG_LIST}"
echo -e "# \n# $(date)\n#" >> "./docs/${PKG_LIST}"
pip freeze | tee -a "./docs/${PKG_LIST}"

# Print message
echo -e "\n\nDon't forget to use \`sudo ./.venv/bin/python ina228_test.py\` to execute!\n"


