from setuptools import setup, find_packages

setup(
    name="apispec-chalice",
    version="0.1.0",
    packages=['apispec_chalice'],
    description='Chalice for the apispec library',
    author='Mathew Marcus',
    author_email='mathewmarcus456@gmail.com',
    install_requires=[
        'apispec>=0.29.0'
    ]
)
