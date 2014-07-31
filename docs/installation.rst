.. _installation:

Installation
============

* To install ::

    pip install django-sendgrid-events

* Add ``'sendgrid_events'`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # other apps
        "sendgrid_events",
    )

* Add ``'sengrid_events.urls'`` as an inclusion to the your main ``urls.py``
  file. You will likely want to provide a bit of security through obscurity
  as you are essentially going to be trusting whatever is POSTed to this url.

  You can do this by generating a UUID and then copy and pasting this as part
  of your URL::

    >>> import uuid
    >>> print uuid.uuid4()
    aeea4b34-e5cb-4b05-84d8-79bfee95ccf4

  Then in your ``urls.py``::

    url("^aeea4b34-e5cb-4b05-84d8-79bfee95ccf4/", include("sendgrid_events.urls"))

* Finally, go to and setup the Events API app, pasting in the end point to this
  url, which will be::

    http(s)://<yoursite.com>/aeea4b34-e5cb-4b05-84d8-79bfee95ccf4/batch/

  Be sure to check the box that says "Batch event notifications"
