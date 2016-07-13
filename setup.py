#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "Django>=1.7,<1.10",
    "Wagtail>=1.4",
]

test_requirements = [
    "Django>=1.8,<1.10",
    "Wagtail>=1.4",
]

setup(
    name='django-wagtail-feeds',
    version='0.0.2',
    description="Support RSS Feeds, Facebook Instant Articles and Apple News",
    long_description=readme + '\n\n' + history,
    author="Christopher Clarke",
    author_email='cclarke@chrisdev.com',
    url='https://github.com/chrisdev/django-wagtail-feeds',
    packages=[
        'wagtail_feeds',
    ],
    package_dir={'wagtail_feeds':
                 'wagtail_feeds'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='wagtail_feeds',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='runtests.runtests',
    tests_require=test_requirements
)
