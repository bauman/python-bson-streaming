#!/usr/bin/python
from setuptools import setup, find_packages

VERSION = "0.1.2"

setup(
    name = "python-bsonstream",
    version = VERSION,
    packages=find_packages(),
    maintainer= 'Dan Bauman',
    maintainer_email='dan@bauman.space',
    license='MIT',
    url = 'https://github.com/bauman/python-bson-streaming',
    download_url = 'https://github.com/bauman/python-bson-streaming/archive/%s.tar.gz' %(VERSION),
    classifiers = [
                       'License :: OSI Approved :: MIT License',
                       'Operating System :: OS Independent',
                       'Programming Language :: Python',
                       'Programming Language :: Python :: 2',
                       'Programming Language :: Python :: 3',
],
)
