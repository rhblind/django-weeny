
.. _installation-label:

Installation
============

    #. Install `django-weeny` using pip or get latest stable release from
       `Bitbucket <https://bitbucket.org/mootacom/django-weeny.git>`_.

       .. code-block:: none

            $ pip install django-weeny

    #. Make sure you have enabled the `django.contrib.sites` and `south`.
    #. Add `weeny` to `INSTALLED_APPS`.

        .. code-block:: python

            INSTALLED_APPS = (
                ...
                'django.contrib.sites',
                'south',
                'weeny',
                ...
            )

    #. Include `weeny.urls.py` in your urlconf.

        .. code-block:: python

            urlpatterns = patterns('',
                ...
                url(r'^weeny/', include("weeny.urls")),
                ...
            )

       .. tip::

            You can use whatever url prefix you'd like for the weeny app.
            For instance, in the current example you would get short urls
            like this: `https://myfantasticsite.com/weeny/PxAwd7/`

    #. Install migrations.

        .. code-block:: none

            $ python manage.py migrate weeny
