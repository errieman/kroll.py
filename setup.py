#!/usr/bin/python
import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = ['requests']

if sys.platform == 'darwin':
 extra_options = dict(
     setup_requires=['py2app'],
     app=[mainscript],
     # Cross-platform applications generally expect sys.argv to
     # be used for opening files.
     options=dict(py2app=dict(argv_emulation=True)),
)

setup(
    name='Kroll',
    version='0.3.46',
    description='CLI weather application',
    long_description=README,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English'],
    author='Erwin Hager',
    author_email='errieman@gmail.com',
    url='https://github.com/errieman/weather.py',
    keywords='weather cli forecast',
    packages=['kroll'],
    include_package_data=True,
    zip_safe=False,
    entry_points="""
    [console_scripts]
    weather = kroll.kroll:main
    forecast = kroll.kroll:main
    """,
    install_requires=requires)