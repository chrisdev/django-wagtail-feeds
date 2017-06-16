Django Wagtail Feeds
====================
.. image:: https://travis-ci.org/chrisdev/django-wagtail-feeds.svg?branch=master
    :target: https://travis-ci.org/chrisdev/django-wagtail-feeds

Support RSS Feeds, JSON Feed, Facebook Instant Articles and Apple News. Syndication feeds come in two flavors:

- **BasicFeed** -  A standard `RSS V 2.0.1`_ feed designed to be used without item enclosures.

- **ExtendedFeed** - An RSS V2/Atom Feed with support for item enclosures such as images or video. Use this if when want to integrate your feed with services like MailChimp or Flipboard.

.. _`RSS V 2.0.1` : http://cyber.law.harvard.edu/rss/rss.html

JSON feed come in two flavors:

- **BasicJsonFeed** -  A standard `JSON feed`_ designed to be used without content html.

- **ExtendedJsonFeed** - A JSON feed with support for content html in items.

.. _`JSON feed` : https://jsonfeed.org/version/1


Getting Started
---------------

To use Django Wagtail Feeds in a project::

    pip install django-wagtail-feeds

Remember to add ``wagtail_feeds`` to installed apps in settings file.

`django-wagtail-feeds` has a dependency on `wagtail settings` app. You must add ``wagtail.contrib.settings`` to your INSTALLED_APPS::

    INSTALLED_APPS += [
        'wagtail.contrib.settings',
        'wagtail_feeds',
    ]

Run migrations for Wagtail feeds::

    ./manage.py migrate wagtail_feeds

Add Feed settings in the Wagtail admin

.. figure:: http://i.imgur.com/aNp1VBg.png
   :alt: Wagtail admin

.. figure:: http://i.imgur.com/oRZRici.png
   :alt: Feed Settings

Finally reference it in the url.py ::

    from wagtail_feeds.feeds import BasicFeed, BasicJsonFeed, ExtendedFeed, ExtendedJsonFeed

    url(r'^blog/feed/basic$', BasicFeed(), name='basic_feed'),
    url(r'^blog/feed/extended$', ExtendedFeed(), name='extended_feed'),

    # JSON feed
    url(r'^blog/feed/basic.json$', BasicJsonFeed(), name='basic_json_feed'),
    url(r'^blog/feed/extended.json$', ExtendedJsonFeed(), name='extended_json_feed'),


Contributing
------------

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.
