import json
from collections import OrderedDict
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import (
    SyndicationFeed,
    rfc3339_date,
    Rss201rev2Feed
)

from wagtail import VERSION as WAGTAIL_VERSION
if WAGTAIL_VERSION >= (2, 0):
    from wagtail.core.models import Site
    from wagtail.core.rich_text import expand_db_html
else:
    from wagtail.wagtailcore.models import Site
    from wagtail.wagtailcore.rich_text import expand_db_html

from datetime import datetime, time
from django.utils.html import strip_tags
from django.apps import apps
from bs4 import BeautifulSoup

try:
    from urlparse import urljoin
except ImportError:  # pragma: no cover
    from urllib.parse import urljoin

from .models import RSSFeedsSettings

try:
    feed_app_settings = RSSFeedsSettings.for_site(
        site=Site.objects.get(is_default_site=True))
    feed_app_label = feed_app_settings.feed_app_label
    feed_model_name = feed_app_settings.feed_model_name
    use_feed_image = feed_app_settings.feed_image_in_content
    feed_item_date_field = feed_app_settings.feed_item_date_field
    is_date_field_datetime = feed_app_settings.is_feed_item_date_field_datetime
except:  # pragma: no cover
    feed_app_settings = None
    feed_item_date_field = None
    is_date_field_datetime = None

try:
    feed_model = apps.get_model(
        app_label=feed_app_label,
        model_name=feed_model_name
    )
except:  # pragma: no cover
    feed_model = None


class CustomFeedGenerator(Rss201rev2Feed):
    def root_attributes(self):
        attrs = super(CustomFeedGenerator, self).root_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attrs

    def add_item_elements(self, handler, item):
        super(CustomFeedGenerator, self).add_item_elements(handler, item)
        handler.startElement(u"content:encoded", {})

        content = '<![CDATA['
        if use_feed_image and item['image'] != "":
            content += '<img src="%s"><hr>' % (item['image'])
        content += item['content']
        content += ']]>'

        # Adding content in this way do not escape content so make it suitable
        # for Feedburner and other services. If we use
        # handler.characters(content) then it will escape content and will not
        # work perfectly with Feedburner and other services.
        handler._write(content)

        handler.endElement(u"content:encoded")


class JSONFeed(SyndicationFeed):
    content_type = 'application/json; charset=utf-8'

    def write(self, outfile, encoding):
        data = OrderedDict()
        data['version'] = 'https://jsonfeed.org/version/1'
        data.update(self.add_root_elements())

        if self.items:
            item_element = []

        for item in self.items:
            item_element += [self.add_item_elements(item), ]

        data['items'] = item_element

        outfile.write(json.dumps(data, encoding=encoding))

    def add_item_elements(self, item):
        item_elements = OrderedDict()

        item_elements['id'] = item['link']
        item_elements['url'] = item['link']
        item_elements['title'] = item['title']
        if item['description'] is not None:
            item_elements['summary'] = item['description']

        content = ''
        if 'image' in item:
            if use_feed_image and item['image'] != "":
                content += '<img src="%s"><hr>' % (item['image'])
        if 'content' in item:
            content += item['content']
            item_elements['content_html'] = content

        if item['pubdate'] is not None:
            item_elements['date_published'] = rfc3339_date(item['pubdate'])

        return item_elements

    def add_root_elements(self):
        root_elements = OrderedDict()

        root_elements['title'] = self.feed['title']
        root_elements['description'] = self.feed['description']
        root_elements['home_page_url'] = self.feed['link']

        if self.feed['feed_url'] is not None:
            root_elements['feed_url'] = self.feed['feed_url']

        if self.feed['author_link'] is not None:
            root_elements['author'] = {'url': self.feed['author_link']}

        return root_elements


class BasicFeed(Feed):
    # FEED TYPE
    feed_type = Rss201rev2Feed

    # The RSS information that gets shown at the top of the feed.
    if feed_app_settings is not None:
        title = feed_app_settings.feed_title
        link = feed_app_settings.feed_link
        description = feed_app_settings.feed_description

        author_email = feed_app_settings.feed_author_email
        author_link = feed_app_settings.feed_author_link

        item_description_field = feed_app_settings.feed_item_description_field
        item_content_field = feed_app_settings.feed_item_content_field

    def items(self):
        if feed_item_date_field:
            return feed_model.objects.live().order_by(
                '-' + feed_item_date_field)
        else:
            return feed_model.objects.live().order_by('-date')

    def item_pubdate(self, item):
        if feed_item_date_field:
            if is_date_field_datetime:
                return getattr(item, feed_item_date_field)
            else:
                return datetime.combine(
                    getattr(item, feed_item_date_field), time())
        else:
            return datetime.combine(item.date, time())

    def item_link(self, item):
        return item.full_url

    def item_author_name(self, item):
        pass


class BasicJsonFeed(BasicFeed):
    # FEED TYPE
    feed_type = JSONFeed

    def item_description(self, item):
        return None


class ExtendedFeed(Feed):
    # FEED TYPE
    feed_type = CustomFeedGenerator

    # The RSS information that gets shown at the top of the feed.
    if feed_app_settings is not None:
        title = feed_app_settings.feed_title
        link = feed_app_settings.feed_link
        description = feed_app_settings.feed_description

        author_email = feed_app_settings.feed_author_email
        author_link = feed_app_settings.feed_author_link

        item_description_field = feed_app_settings.feed_item_description_field
        item_content_field = feed_app_settings.feed_item_content_field

    def get_site_url(self):
        site = Site.objects.get(is_default_site=True)
        return site.root_url

    def items(self):
        if feed_item_date_field:
            return feed_model.objects.live().order_by(
                '-' + feed_item_date_field)
        else:
            return feed_model.objects.live().order_by('-date')

    def item_pubdate(self, item):
        if feed_item_date_field:
            if is_date_field_datetime:
                return getattr(item, feed_item_date_field)
            else:
                return datetime.combine(
                    getattr(item, feed_item_date_field), time())
        else:
            return datetime.combine(item.date, time())

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        content = strip_tags(getattr(item, self.item_description_field))
        return content

    def item_link(self, item):
        return item.full_url

    def item_author_name(self, item):
        pass

    def item_extra_kwargs(self, item):
        """
        Returns an extra keyword arguments dictionary that is used with
        the 'add_item' call of the feed generator.
        Add the fields of the item, to be used by the custom feed generator.
        """
        if use_feed_image:
            feed_image = item.feed_image
            if feed_image:
                image_complete_url = urljoin(
                    self.get_site_url(), feed_image.file.url
                )
            else:
                image_complete_url = ""

        content_field = getattr(item, self.item_content_field)
        try:
            content = expand_db_html(content_field)
        except:
            content = content_field.__html__()

        soup = BeautifulSoup(content, 'html.parser')
        # Remove style attribute to remove large botton padding
        for div in soup.find_all("div", {'class': 'responsive-object'}):
            del div['style']
        # Add site url to image source
        for img_tag in soup.findAll('img'):
            if img_tag.has_attr('src'):
                img_tag['src'] = urljoin(self.get_site_url(), img_tag['src'])

        fields_to_add = {
            'content': soup.prettify(formatter="html"),
        }

        if use_feed_image:
            fields_to_add['image'] = image_complete_url
        else:
            fields_to_add['image'] = ""

        return fields_to_add


class ExtendedJsonFeed(ExtendedFeed):
    # FEED TYPE
    feed_type = JSONFeed
