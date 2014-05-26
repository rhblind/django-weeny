# -*- coding: utf-8 -*-

from distutils.core import setup


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
    package_data={
        "weeny": [
            "locale/*/*",
            "static/weeny/img/*",
            "static/weeny/css/*.css",
            "templates/weeny/*.html"
        ]
    },
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: Unspecified :: Apache",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4"
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
