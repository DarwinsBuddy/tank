import os
import subprocess
import sys
from distutils.command.install import install

from setuptools import setup, find_packages
from setuptools._distutils import cmd

RESOURCES = "resources"
WEBAPP = "webapp"
MODULE = "tank"


class NpmCommand(cmd.Command):
    """A custom command to run Pylint on all Python source files."""

    description = 'run npm install & build'
    user_options = [
        # The format is (long option, short option, description).
        ('webapp_path=', "wp=", 'path to webapp'),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.webapp_path = "./tank/resources/webapp"

    def finalize_options(self):
        """Post-process options."""
        if self.webapp_path:
            print(os.getcwd())
            assert os.path.exists(self.webapp_path), (
                f"webapp path '{self.webapp_path}' does not exist.")

    def run(self):
        """Run command."""
        if not self.webapp_path:
            print("No webapp path specified. Aborting...")
            sys.exit(1)
        wd = os.getcwd()
        os.chdir(self.webapp_path)
        npm_install = ['/usr/bin/npm', 'install']
        npm_build = ['/usr/bin/npm', 'run', 'build']
        self.announce(str(npm_install))
        subprocess.check_call(npm_install)
        self.announce(str(npm_build))
        subprocess.check_call(npm_build)
        os.chdir(wd)


class InstallWrapper(install):
    def run(self):
        # fist run npm install and build to build our webapp
        self.run_command("build-client")
        # now run install :)
        install.run(self)


setup(
    name=f'{MODULE}',
    author="Christoph Spörk",
    author_email="christoph.spoerk@gmail.com",
    platforms="any",
    version='0.1.0',
    packages=find_packages(
        include=[f'{MODULE}', f'{MODULE}.*']
    ),
    package_data={"tank": [
        "resources/webapp/dist/assets/*",
        "resources/webapp/dist/index.html"
        "resources/tank.service"
    ]},
    cmdclass={
        'install': InstallWrapper,
        'build-client': NpmCommand
    },
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
