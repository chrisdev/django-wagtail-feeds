=======
History
=======
0.0.8 (2017-06-26)
------------------
* Provide initial support for `JSON Feed_`. 

    The JSON Feed format is a pragmatic syndication format, like RSS and Atom, but with one big difference: it’s JSON instead of XML.  

.. _`JSON Feed` : https://jsonfeed.org/version/1


0.0.7 (2017-05-22)
------------------
* Support for Django 1.11 and Wagtail 1.10.1
* Temporarily reduce test coverage

0.0.6 (2016-10-06)
------------------
* More comprehensive test coverage  

0.0.5 (2016-10-05)
------------------
* Added tests for StreamFields

0.0.4 (2016-09-29)
-------------------
* The `ExtendedFeed` now supports content fields based on StreamFields
* Previous versions automatically added the post/article's feed image to the content
  enclosure. In this version, this can be toggled on or off with 
  a checkbox option in the Feed App Settings
* Several bug fixes related to issues such the rendering of embedded objects in posts
  and improperly formatted images

0.0.3 (2016-07-18)
------------------
* Needed to pin html5lib version due to problems with BS4    

0.0.2 (2016-07-13)
------------------

* First release on PyPI.
