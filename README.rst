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


Compatibility checkpoint (unreleased)
------------------------------------

The ``codex/wagtail-5-compat`` branch updates removed Wagtail namespace imports,
uses ``BaseSiteSetting`` where available (with a fallback for earlier Wagtail),
and uses Django's ``gettext_lazy``. No feed format or configuration behaviour is
changed. This is a source compatibility checkpoint, not a new PyPI release.
Its development version is ``0.1.1.dev1`` so installers distinguish it from
the existing ``0.1.0`` release.

The earlier eight-test checkpoint passed on Python 3.8.10 / Django 3.2.25
with both Wagtail 4.1.9 and 5.2.8. The Django 4 follow-up has nine tests passing
on Wagtail 5.2.8 with Django 3.2.25 and 4.2.30. They include feed properties, StreamField content, absolute
inline image URLs and the feed image. Tests use an in-memory SQLite database
and temporary media via ``python runtests.py``. Imports and fixtures in the
test suite now target modern Wagtail; other historical combinations have not
been revalidated. The Ministry application's PostgreSQL integration tests also
exercise basic/extended RSS output, live filtering, ordering, URLs and dates.

Site/feed settings are still captured at module import. Restart the application
after changing them; changing that behaviour is outside this compatibility fix.

The Django 4 follow-up closes the XML writer's pending ``content:encoded`` start
tag before writing CDATA. It preserves the existing CDATA representation while
avoiding malformed RSS with Django's short-empty-element writer. A regression
test parses the generated feed and checks its embedded HTML and image content.

Getting Started
---------------

**The latest release (0.1.0) breaks backward compatibility  with previous versions of Wagtail which were baseed Django 1.x. Use 0.0.8 for projects based on older versions of Wagtail**

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
