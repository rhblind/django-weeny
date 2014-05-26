
.. _usage-label:

Usage
=====

Add a Weeny Site
----------------

The `weeny` is using the `django.contrib.sites` app in order to wire up URL's.

#. In the django admin interface, click the `Add new weeny site` icon to get started.

    .. image:: images/add_weeny_site1.png

#. **Site**

   From the drop-down, select the site you wish to associate your URL's with.
   It is important that this domain is the domain you are hosting your site on.
   When URL redirection occurs, this is the domain which will be used.

    .. image:: images/add_weeny_site2.png

#. **Short domain name**

   Enter the short domain name for this site. This option is not used unless you check the `Redirect to short domain`
   option below. You'll also need to register a real hostname and make sure it points to this site for this to work.

#. **Redirect to short domain**

   Check this if you want your URL's to redirect to this domain name instead of the `Site` domain name.

#. **Protocol**

   Choose what transport protocol you want the URL's for this site to use.

#. **Track**

   The `Track` option specifies whether you want to track *ALL* URL's for this domain.

#. The read-only attribute `Seed` is a unique seed which will be used to generate URL's
   for this domain.


Add a Weeny URL
---------------

Next step is to add a URL.

#. Click the `Add new Weeny URL` icon to get started.

    .. image:: images/add_weeny_url1.png

#. From the drop-down list, choose your `weeny site`.

    .. image:: images/add_weeny_url2.png

#. Content type and Object ID

    .. tip::

        If you are not familiar with the Content-Types framework, you might want to read
        a little about it. It's awesome, and one of my favorite django features! In short it
        is a way of creating `Generic relations` between objects, which means that we can have
        database relations between any models we'd like without knowing anything about them beforehand.
        The only requirements is that you know what kind of object it is, and the `primary key` of the
        requested object.

    Choose your model and object ID.

    .. warning::

        The target content object *must* have a `get_absolute_url` method implemented!

#. URL code

    This is the code you'll append to the short-url.

    For instance, if you wired up `weeny.urls.py` to `/weeny/`, the short URL for this
    object would be `/weeny/l/`.

#. Privacy and moderation options

    .. image:: images/add_weeny_url3.png

    These options should be pretty self-explanatory.

    - **Private URL**

      Check this if you'd like user to enter a password to complete the redirect. You'll
      also need to enter a password in the password field below.

    - **Track**

      Enable URL tracking for this URL. If URL tracking is enabled on the related Weeny site,
      this option does nothing.

    - **Active**

      Inactive URL's does not work!

    - **Allow revisit**

      Uncheck to make URL single use.
