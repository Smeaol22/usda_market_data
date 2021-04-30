# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    my_license = f.read()

setup(
    name='name of your project',
    version='0.1.0',
    description='put your description',
    long_description=readme,
    author='Dauloudet Olivier',
    url='https://github.com/Smeaol22/****',
    license=my_license,
    packages=find_packages(exclude=('tests', 'docs', 'example', 'conda'))
)
