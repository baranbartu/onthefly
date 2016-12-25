#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
from onthefly import __version__

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

packages = find_packages()

setup(
    name='django-onthefly',
    version=__version__,
    description='Change Django Settings On the Fly',
    long_description=README,
    url='https://github.com/baranbartu/onthfly',
    download_url='https://github.com/baranbartu/onthfly/tarball/%s' % (
        __version__,),
    author='Baran Bartu Demirci',
    author_email='bbartu.demirci@gmail.com',
    license='MIT',
    keywords='django,settings,change django settings',
    packages=packages,
    package_data={'onthefly': ['templates/admin/onthefly_settings.html']},
    include_package_data=True,
    install_requires=[
        'Django>=1.7',
        'django-adminplus>=0.5',
        'redis>=2.10.5'
    ]
)
