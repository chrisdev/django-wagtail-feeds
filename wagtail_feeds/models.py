from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.contrib.settings.models import (
    BaseSetting,
    register_setting
)


# Create your models here.


@register_setting
class RSSFeedsSettings(BaseSetting):
    feed_app_label = models.CharField(
        _('Feed app label'),
        max_length=255,
        help_text=_('blog App whose Feed is to be generated'),
        null=True,
        blank=True
    )
    feed_model_name = models.CharField(
        _('Feed model name'),
        max_length=255,
        help_text=_('Model to be used for feed generation'),
        null=True,
        blank=True
    )
    feed_title = models.CharField(
        _('Feed title'), max_length=255, help_text=_('Title of Feed'), null=True, blank=True
    )
    feed_link = models.URLField(
        _('Feed link'), max_length=255, help_text=_('link for Feed'), null=True, blank=True
    )
    feed_description = models.CharField(
        _('Feed description'),
        max_length=255,
        help_text=_('Description of field'),
        null=True,
        blank=True
    )
    feed_author_email = models.EmailField(
        _('Feed author email'),
        max_length=255,
        help_text=_('Email of author'),
        null=True,
        blank=True
    )
    feed_author_link = models.URLField(
        _('Feed author link'),
        max_length=255,
        help_text=_('Link of author'),
        null=True,
        blank=True
    )

    feed_item_description_field = models.CharField(
        _('Feed item description field'),
        max_length=255,
        help_text=_('Description field for feed item'),
        null=True,
        blank=True
    )
    feed_item_content_field = models.CharField(
        _('Feed item content field'),
        max_length=255,
        help_text=_('Content Field for feed item'),
        null=True,
        blank=True
    )
    feed_image_in_content = models.BooleanField(
        _('Feed image in content'),
        help_text=_('Add feed image to content encoded field'),
        default=True
    )
    feed_item_date_field = models.CharField(
        _('Feed item date field'),
        max_length=255,
        help_text=_('(Optional). Date Field for feed item. By default use date'),
        blank=True
    )
    is_feed_item_date_field_datetime = models.BooleanField(
        _('Is Feed item date field Datetime Field'),
        help_text=_('If the above date field is DateTime field, tick this.'),
        default=False
    )

    class Meta:
        verbose_name = _('RSS feed setting')
        verbose_name_plural = _('RSS feed settings')
