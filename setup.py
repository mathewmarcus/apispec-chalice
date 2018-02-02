from setuptools import setup, find_packages
from importlib import import_module
import os.path

setup(
    name="apispec-chalice",
    version="0.1.1",
    packages=['apispec_chalice'],
    description='Chalice for the apispec library',
    author='Mathew Marcus',
    author_email='mathewmarcus456@gmail.com',
)

try:
    apispec_ext_package = os.path.dirname(import_module('apispec.ext').__file__)
    link_name = os.path.join(apispec_ext_package, 'chalice.py')

    target = import_module('apispec_chalice.chalice').__file__
    os.symlink(target, link_name)
except ImportError:
    pass
except FileExistsError:
    os.remove(link_name)
    os.symlink(target, link_name)
