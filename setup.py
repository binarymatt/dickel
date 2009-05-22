#!/usr/bin/env python
# encoding: utf-8
import os
from setuptools import setup, find_packages
 
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
 
setup(
    name = "dickel",
    version = "0.2",
    url = 'http://github.com/binarydud/dickel',
    license = 'MIT',
    description = "A barebones wsgi framework",
    long_description = read('README.rst'),
 
    author = 'Matt George',
    author_email = 'mgeorge@gmail.com',
 
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    
    install_requires = ['setuptools','webob','webtest'],
 
)
