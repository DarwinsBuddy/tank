# tank

# Dependencies

## Building
* npm / node 16.6.2
* python3.9+
* pip
* wheel
## Build
```
pip install wheel
python setup.py bdist_wheel
```
install wheel
`pip install tank-x.x.x-py3-none-any.whl`
## Install
* (optional) systemd

# Install / Start

## systemd
1. `sudo ./install.sh`
2. browse to `127.0.0.1:8080`
> service name: `tank.service`
## only as python module
`python setup.py install`

`python -m tank`
# Uninstall
## systemd
`sudo ./uninstall.sh`
## only as python module
`pip uninstall tank`