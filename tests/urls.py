from django.urls import include, re_path

from wagtail import urls as wagtail_urls

from wagtail_feeds.feeds import BasicFeed, ExtendedFeed


urlpatterns = [
    re_path(r'^blog/feed/basic$', BasicFeed(), name='basic_feed'),
    re_path(r'^blog/feed/extended$', ExtendedFeed(), name='extended_feed'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    re_path(r'', include(wagtail_urls))
]
