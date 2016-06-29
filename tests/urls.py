from django.conf.urls import include, url

from wagtail.wagtailcore import urls as wagtail_urls

from wagtail_feeds.feeds import BasicFeed, ExtendedFeed


urlpatterns = [
    url(r'^blog/feed/basic$', BasicFeed(), name='basic_feed'),
    url(r'^blog/feed/extended$', ExtendedFeed(), name='extended_feed'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    url(r'', include(wagtail_urls)),
]
