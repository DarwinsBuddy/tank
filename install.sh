#!/bin/bash

PACKAGE=tank
WEBAPP=./webapp

# install and build webapp
cd "${PACKAGE}/${WEBAPP}" && \
npm install && \
npm run build &&
cd ../..
# install and build python-server
python3 -m venv ./venv
./venv/bin/python setup.py install
# copy service file into systemd

# enable and start service
