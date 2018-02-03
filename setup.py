from setuptools import setup, find_packages
from importlib import import_module
import os.path

setup(
    name="apispec-chalice",
    version="0.2.2",
    packages=['apispec_chalice'],
    description='Chalice plugin for the apispec library',
    author='Mathew Marcus',
    author_email='mathewmarcus456@gmail.com',
    long_description=open('README.rst').read(),
    install_requires=['apispec>=0.29.0']
)
