Usage
=====

To use Django Wagtail Feeds in a project::

    import wagtail_feeds
    
Run migrations for Wagtail feeds::

    ./manage.py migrate wagtail_feeds
    
Add Feed settings in the Wagtail admin

.. image:: /_static/images/admin.png
   
.. image:: /_static/images/feed-settings.png

Finally reference it in the url.py ::
    
    from wagtail_feeds.feeds import BasicFeed, ExtendedFeed
    
    url(r'^blog/feed/basic$', BasicFeed(), name='basic_feed'),
    url(r'^blog/feed/extended$', ExtendedFeed(), name='extended_feed'),