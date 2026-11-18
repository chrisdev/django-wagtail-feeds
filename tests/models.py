from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock


class HomePage(Page):
    pass


class BlogPage(Page):
    intro = RichTextField()
    body = RichTextField()
    date = models.DateField("Post date")

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


class BlogStreamPage(Page):
    intro = RichTextField()
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True)
    date = models.DateField("Post date")

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
