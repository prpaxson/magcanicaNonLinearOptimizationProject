# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='nlop',
    version='0.1.0',
    description='Non-Linear Optimization Problem',
    long_description=readme,
    author='Michael Callahan',
    url='https://github.com/mikewcallahan/nonLinearOptimizationProject',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

