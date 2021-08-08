from setuptools import setup, find_packages

setup(
    name='tank',
    version='0.1.0',
    packages=find_packages(include=['tank', 'tank.*']),
    package_data={'webapp': ['webapp']},
    install_requires=[
        'APScheduler==3.7.0',
        'bidict==0.21.2',
        'click==8.0.1',
        'Flask==2.0.1',
        'Flask-APScheduler==1.12.2',
        'Flask-Cors==3.0.10',
        'Flask-SocketIO==5.1.1',
        'itsdangerous==2.0.1',
        'Jinja2==3.0.1',
        'MarkupSafe==2.0.1',
        'python-dateutil==2.8.2',
        'python-engineio==4.2.1',
        'python-socketio==5.4.0',
        'pytz==2021.1',
        'pyzmq==22.2.1',
        'six==1.16.0',
        'tzlocal==2.1',
        'Werkzeug==2.0.1'
    ]
)
