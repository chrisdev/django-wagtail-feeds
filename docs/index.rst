.. wagtail_feeds documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django Wagtail Feeds
====================

Support RSS Feeds, Facebook Instant Articles and Apple News

Syndication feeds come in two flavors:

 - **BasicFeed** -  A standard `RSS V 2.0.1`_ feed designed to be used without 
   item enclosures.

 - **ExtendedFeed** - An RSS V2/Atom Feed with support for item  
   enclosures such as images or video. Use this if when want to integrate your
   feed with services like MailChimp or Flipboard.


.. _`RSS V 2.0.1` : http://cyber.law.harvard.edu/rss/rss.html


.. _getting_started:

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   usage 

.. _contributing:

.. toctree::
   :maxdepth: 2
   :caption: Project Info

   project_info/contributing
   project_info/authors