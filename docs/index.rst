.. _toc-label:

Table of Contents
=================

.. toctree::
    :maxdepth: 2

    installation
    usage

About
=====

Django-Weeny is a small and simple URL shortener app for Django.
It supports basic features like:

    - Creating short-URL's for any database object through Generic Relations
    - URL tracking
    - Password protection for single URL's


Planned features
----------------

    - Moderation system
    - Template tags for resolving short-URL's
    - Basic statistics through the django admin interface
    - Admin actions for various administration actions


Requirements
------------

**Python packages**

The python requirements are automatically installed if installing with `pip` or running
`python setup.py install` using the source distribution.

    - `Django >= 1.5.0`
    - `PyYAML`
    - `South`
    - `ua-parser`
    - `user-agents`

**Django apps**

Django-Weeny requires the following django apps to be enabled:

    - `django.contrib.sites`
    - `django.contrib.contenttypes`
    - `south`


Want to contribute?
===================

We'd love django-weeny to get even better!

Submit your patches at `Bitbucket <https://bitbucket.org/mootacom/django-weeny.git>`_!


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

