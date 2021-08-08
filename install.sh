#!/bin/bash

python3 -m venv ./venv
# TODO: run npm install
# TODO: npm run build
./venv/bin/python setup.py install
# TODO: copy service file into systemd
# TODO: enable and start service
