#!/usr/bin/env python

import os
import sys
import django

from django.conf import settings


class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"


if not settings.configured:
    settings_dict = dict(
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sites',

            'wagtail.contrib.wagtailstyleguide',
            'wagtail.contrib.wagtailsitemaps',
            'wagtail.contrib.wagtailroutablepage',
            'wagtail.contrib.wagtailfrontendcache',
            'wagtail.contrib.wagtailsearchpromotions',
            'wagtail.contrib.settings',
            'wagtail.contrib.modeladmin',
            'wagtail.contrib.table_block',
            'wagtail.wagtailforms',
            'wagtail.wagtailsearch',
            'wagtail.wagtailembeds',
            'wagtail.wagtailimages',
            'wagtail.wagtailsites',
            'wagtail.wagtailusers',
            'wagtail.wagtailsnippets',
            'wagtail.wagtaildocs',
            'wagtail.wagtailadmin',
            'wagtail.wagtailcore',

            'taggit',

            'wagtail_feeds',
            'tests',
        ),
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "memory",
                "USER": "",
                "PASSWORD": "",
                "HOST": "",
                "PORT": "",
            }
        },
        MIGRATION_MODULES=DisableMigrations(),
        MIDDLEWARE_CLASSES=(),
        WAGTAIL_SITE_NAME="Test Site",
        ROOT_URLCONF='tests.urls',
        SITE_ID=1,
    )

    settings.configure(**settings_dict)
    if django.VERSION >= (1, 7):
        django.setup()


def runtests(*test_args):
    if not test_args:
        test_args = ['tests']

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    if django.VERSION < (1, 8):
        from django.test.simple import DjangoTestSuiteRunner
        failures = DjangoTestSuiteRunner(
            verbosity=1, interactive=True, failfast=False).run_tests(['tests'])
        sys.exit(failures)

    else:
        from django.test.runner import DiscoverRunner
        failures = DiscoverRunner(
            verbosity=1, interactive=True, failfast=False).run_tests(test_args)
        sys.exit(failures)


if __name__ == '__main__':
    runtests()
