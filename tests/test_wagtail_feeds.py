from django.test import TestCase
from django.apps import apps
from django.core.urlresolvers import reverse

from wagtail.wagtailcore.rich_text import RichText
from wagtail.wagtailcore.models import Collection, Page
from wagtail.wagtailimages.tests.utils import Image, get_test_image_file

from wagtail_feeds.models import RSSFeedsSettings
from wagtail_feeds.feeds import (
    BasicFeed, BasicJsonFeed, ExtendedFeed, ExtendedJsonFeed,
)

from .models import HomePage, BlogPage, BlogStreamPage


class WagtailFeedTests(TestCase):
    def setUp(self):
        ContentType = apps.get_model('contenttypes.ContentType')
        Site = apps.get_model('wagtailcore.Site')

        # Delete the default homepage
        Page.objects.get(id=2).delete()

        # Create content type for homepage model
        homepage_content_type, created = ContentType.objects.get_or_create(
            model='HomePage', app_label='tests')

        # Create a new homepage
        homepage = HomePage.objects.create(
            title="Homepage",
            slug='home',
            content_type=homepage_content_type,
            path='00010001',
            depth=1,
            url_path="/home-page",
        )

        # Create a site with the new homepage set as the root
        site = Site.objects.create(
            hostname='localhost', root_page=homepage, is_default_site=True)

        RSSFeedsSettings.objects.create(
            site=site, feed_app_label='tests',
            feed_model_name='BlogStreamPage',
            feed_title='Test Feed',
            feed_link="https://example.com",
            feed_description="Test Description",
            feed_item_description_field="intro",
            feed_item_content_field="body",
            feed_image_in_content=True
        )

        # Create collection for image
        img_collection = Collection.objects.create(name="test", depth=1)

        # Create an image
        image = Image.objects.create(
            title="Test image",
            file=get_test_image_file(),
            collection=img_collection,
        )

        blogpage_content_type, created = ContentType.objects.get_or_create(
            model='BlogPage', app_label='tests')

        # Create Blog Page
        BlogPage.objects.create(
            title="BlogPage",
            intro="Welcome to Blog",
            body="This is the body of blog",
            date="2016-06-30",
            slug='blog-post',
            url_path="/home-page/blog-post/",
            content_type=blogpage_content_type,
            feed_image=image,
            path='000100010002',
            depth=2,
        )

        stream_blogpage_content_type, created = ContentType.objects.get_or_create(
            model='BlogStreamPage', app_label='tests')

        # Create Stream Field Blog Page

        stream_page = BlogStreamPage.objects.create(
            title="BlogStreamPage",
            intro="Welcome to Blog Stream Page",
            body=[
            ('heading', 'foo'),
            ('paragraph', RichText(
                '<p>Rich text</p><div style="padding-bottom: 56.25%;"' +
                ' class="responsive-object"> <iframe width="480" height="270"' +
                ' src="https://www.youtube.com/embed/mSffkWuCkgQ?feature=oembed"' +
                ' frameborder="0" allowfullscreen=""></iframe>' +
                '<img alt="wagtail.jpg" height="500"' +
                ' src="/media/images/wagtail.original.jpg" width="1300">' +
                '</div>'))],
            date="2016-08-30",
            slug='blog-stream-post',
            url_path="/home-page/blog-stream-post/",
            content_type=stream_blogpage_content_type,
            feed_image=image,
            path='000100010003',
            depth=3,
        )

    def test_settings_values(self):
        feed_settings = RSSFeedsSettings.objects.first()
        self.assertEqual(feed_settings.feed_app_label, 'tests')
        self.assertEqual(feed_settings.feed_model_name, 'BlogStreamPage')
        self.assertEqual(feed_settings.feed_title, 'Test Feed')
        self.assertEqual(feed_settings.feed_item_description_field, 'intro')
        self.assertEqual(feed_settings.feed_item_content_field, 'body')

    def test_blog_values(self):
        blog = BlogPage.objects.first()
        self.assertEqual(blog.intro, 'Welcome to Blog')
        self.assertEqual(blog.body, 'This is the body of blog')

    def test_stream_blogpage_values(self):
        stream_blogpage = BlogStreamPage.objects.first()
        body = stream_blogpage.body
        self.assertEqual(body[0].value, 'foo')
        self.assertIsInstance(body[1].value, RichText)
        self.assertHTMLEqual(
            body[1].value.source,
            '<p>Rich text</p><div style="padding-bottom: 56.25%;"' +
            ' class="responsive-object"> <iframe width="480" height="270"' +
            ' src="https://www.youtube.com/embed/mSffkWuCkgQ?feature=oembed"' +
            ' frameborder="0" allowfullscreen=""></iframe>' +
            '<img alt="wagtail.jpg" height="500"' +
            ' src="/media/images/wagtail.original.jpg" width="1300">' +
            '</div>'
        )

    def test_basic_rss_feed(self):
        blog = BlogPage.objects.first()
        basic_rss_feed = BasicFeed()

        self.assertEqual(
            basic_rss_feed.item_title(blog),
            blog.title
        )
        self.assertEqual(
            basic_rss_feed.item_pubdate(blog).date(),
            blog.date
        )
        self.assertEqual(
            basic_rss_feed.item_link(blog),
            blog.full_url
        )

    def test_basic_json_feed(self):
        blog = BlogPage.objects.first()
        basic_json_feed = BasicJsonFeed()

        self.assertEqual(
            basic_json_feed.item_title(blog),
            blog.title
        )
        self.assertEqual(
            basic_json_feed.item_pubdate(blog).date(),
            blog.date
        )
        self.assertEqual(
            basic_json_feed.item_link(blog),
            blog.full_url
        )

    def test_extended_rss_feed(self):
        blog = BlogPage.objects.first()
        extended_rss_feed = ExtendedFeed()

        self.assertEqual(
            extended_rss_feed.item_title(blog),
            blog.title
        )
        self.assertEqual(
            extended_rss_feed.item_pubdate(blog).date(),
            blog.date
        )
        self.assertEqual(
            extended_rss_feed.item_link(blog),
            blog.full_url
        )

    def test_extended_json_feed(self):
        blog = BlogPage.objects.first()
        extended_json_feed = ExtendedJsonFeed()

        self.assertEqual(
            extended_json_feed.item_title(blog),
            blog.title
        )
        self.assertEqual(
            extended_json_feed.item_pubdate(blog).date(),
            blog.date
        )
        self.assertEqual(
            extended_json_feed.item_link(blog),
            blog.full_url
        )

    #def test_rss_basic_generation(self):
    #    response = self.client.get(reverse('basic_feed'))
    #    self.assertEqual(response.status_code, 200)

    #def test_rss_extended_generation(self):
    #    response = self.client.get(reverse('extended_feed'))
    #    self.assertEqual(response.status_code, 200)

    #def test_rss_extended_generation_without_feed_image(self):
    #    stream_page = BlogStreamPage.objects.first()
    #    stream_page.feed_image = None
    #    stream_page.save()
    #    response = self.client.get(reverse('extended_feed'))
    #    self.assertEqual(response.status_code, 200)
