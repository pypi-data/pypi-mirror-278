from os.path import abspath, dirname, join
from setuptools import setup, find_packages

with open(join(dirname(abspath(__file__)), 'requirements.txt'), encoding='utf-8') as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    name = 'robotframework-xray',
    version = '1.0.0',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = REQUIREMENTS,
)