import os
from setuptools import setup, find_packages

# Specify the path to your requirements.txt file
requirements_path = 'JaysAppManager/requirements.txt'

# Read the requirements from the file
with open(requirements_path) as f:
    requirements = f.read().splitlines()


build_num = os.getenv('CIRCLE_BUILD_NUM', '0')


VERSION = f'0.0.{build_num}'
DESCRIPTION = 'A helpful appmanager'
LONG_DESCRIPTION = 'A helpful appmanager'

setup(
    name="JaysAppManager",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Jay Fesco",
    author_email="jayfesco1@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ping = funtions.log:ping',
            'register = funtions.register:register',
        ],
    },
)