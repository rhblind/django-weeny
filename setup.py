# -*- coding: utf-8 -*-

from ez_setup import use_setuptools
from setuptools import setup

use_setuptools()

setup(
    name="django-weeny",
    version="1.0",
    url="https://bitbucket.org/mootacom/django-weeny",
    download_url="https://rhblind@bitbucket.org/mootacom/django-weeny.git",
    license=open("LICENSE.rst", "r").read(),
    author="Rolf Håvard Blindheim",
    author_email="rhblind@gmail.com",
    description="Small URL shortner app for django.",
    long_description=open("README.rst", "r").read(),
    packages=[
        "weeny",
        "weeny.forms",
        "weeny.migrations",
        "weeny.tests"
    ],
    include_package_data=True,
    install_requires=[
        "Django>=1.5.0",
        "PyYAML",
        "South",
        "ua-parser",
        "user-agents"
    ],
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
