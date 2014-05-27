# -*- coding: utf-8 -*-

from setuptools import setup

import ez_setup
ez_setup.use_setuptools()


setup(
    name="django-weeny",
    version="1.0.2",
    url="https://bitbucket.org/mootacom/django-weeny",
    download_url="https://rhblind@bitbucket.org/mootacom/django-weeny.git",
    license="Apache Software License",
    author="Rolf Håvard Blindheim",
    author_email="rhblind@gmail.com",
    description="Small and simple URL shortener app for Django.",
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
    py_modules=["ez_setup"],
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
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
