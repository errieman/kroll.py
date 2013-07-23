#!/usr/bin/python
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'requests',
    'cPickle']

setup(
    name='Krol',
    version='0.3.21',
    description='CLI weather application',
    long_description=README,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English']
    author='Erwin Hager',
    author_email='errieman@gmail.com',
    url='https://github.com/errieman/weather.py',
    keywords='weather cli forecast',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires)