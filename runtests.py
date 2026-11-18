#!/usr/bin/env python

import os
import sys
from tempfile import TemporaryDirectory

import django
from django.conf import settings
from django.test.utils import get_runner


def runtests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    with TemporaryDirectory(prefix='wagtail-feeds-tests-') as media:
        settings.MEDIA_ROOT = media
        failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()
