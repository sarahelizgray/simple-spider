Spider
======
A spider that relies on google sitemap.xml to look for broken links in your site.

### Setup
```
sudo pip install requests

sudo pip install beautifulsoup4

sudo pip install mox

sudo pip install requests_testadapter

sudo pip install lxml

```
* You may need to use STATIC_DEPS=true pip install lxml if beautiful soup fails to recognize your lxml parser much love to [roderickhodgson](http://roderickhodgson.com/blog/2012/10/27/building-python-lxml-on-mac-os-x-10-dot-7) and [the lxml docs](http://lxml.de/installation.html) for indenfitying this fix.

### To Do
* use list of site pages to collect all links across the domain
* enforce uniqueness in the collection of all links
* format urls to they are uniform
* hit all links in sanitized list
* generate an email report based on the spider results
* exclude spider from analytics
