import json
from django.test import TestCase
from django.apps import apps
from django.core.urlresolvers import reverse

from wagtail.wagtailcore.rich_text import RichText

from wagtail_feeds.models import RSSFeedsSettings

from .models import HomePage, BlogPage, BlogStreamPage


class WagtailFeedTests(TestCase,):
    def setUp(self):
        ContentType = apps.get_model('contenttypes.ContentType')
        Site = apps.get_model('wagtailcore.Site')

        # Create content type for homepage model
        homepage_content_type, created = ContentType.objects.get_or_create(
            model='homepage', app_label='tests')

        # Create a new homepage
        homepage = HomePage.objects.create(
            title="Homepage",
            slug='home',
            content_type=homepage_content_type,
            path='0001',
            depth=1,
            url_path="/home-page",
        )

        # Create a site with the new homepage set as the root
        site = Site.objects.create(
            hostname='localhost', root_page=homepage, is_default_site=True)

        RSSFeedsSettings.objects.create(site=site, feed_app_label='tests',
                                        feed_model_name='BlogPage',
                                        feed_title='Test Feed',
                                        feed_link="https://example.com",
                                        feed_description="Test Description",
                                        feed_item_description_field="intro",
                                        feed_item_content_field="body")

        blogpage_content_type, created = ContentType.objects.get_or_create(
            model='blogpage', app_label='tests')

        # Create Blog Page
        BlogPage.objects.create(
            title="BlogPage",
            intro="Welcome to Blog",
            body="This is the body of blog",
            date="2016-06-30",
            slug='blog-post',
            url_path="/home-page/blog-post/",
            content_type=homepage_content_type,
            path='00010002',
            depth=2,
        )

        # Create Stream Field Blog Page


        stream_page = BlogStreamPage.objects.create(
            title="BlogStreamPage",
            intro="Welcome to Blog Stream Page",
            body=[
            ('heading', 'foo'),
            ('paragraph', RichText('<p>Rich text</p>'))],
            date="2016-08-30",
            slug='blog-stream-post',
            url_path="/home-page/blog-stream-post/",
            content_type=homepage_content_type,
            path='00010003',
            depth=3,
        )

    def test_settings_values(self):
        feed_settings = RSSFeedsSettings.objects.all()[0]
        self.assertEqual(feed_settings.feed_app_label, 'tests')
        self.assertEqual(feed_settings.feed_model_name, 'BlogPage')
        self.assertEqual(feed_settings.feed_title, 'Test Feed')
        self.assertEqual(feed_settings.feed_item_description_field, 'intro')
        self.assertEqual(feed_settings.feed_item_content_field, 'body')

    def test_blog_values(self):
        blog = BlogPage.objects.all()[0]
        self.assertEqual(blog.intro, 'Welcome to Blog')
        self.assertEqual(blog.body, 'This is the body of blog')

    def test_stream_page(self):
        stream_blogpage = BlogStreamPage.objects.all()[0]
        body = stream_blogpage.body
        self.assertEqual(body[0].value, 'foo')
        self.assertIsInstance(body[1].value, RichText)
        self.assertEqual(body[1].value.source, '<p>Rich text</p>')

    def test_rss_basic_generation(self):
        response = self.client.get(reverse('basic_feed'))
        self.assertEqual(response.status_code, 200)

    def test_rss_extended_generation(self):
        response = self.client.get(reverse('extended_feed'))
        self.assertEqual(response.status_code, 200)
