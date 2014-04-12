Spider
======
A spider that relies on google sitemap.xml to look for broken links in your site.

###Spider construction
Why xml and lxml?
http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser

### Setup
Make sure that your site has sitemap.xml at the root of your domain.

```
sudo pip install requests

sudo pip install beautifulsoup4

sudo pip install mox

sudo pip install requests_testadapter

sudo pip install freezegun

sudo pip install lxml

```
* You may need to use STATIC_DEPS=true pip install lxml if beautiful soup fails to recognize your lxml parser much love to [roderickhodgson](http://roderickhodgson.com/blog/2012/10/27/building-python-lxml-on-mac-os-x-10-dot-7) and [the lxml docs](http://lxml.de/installation.html) for indenfitying this fix.

### To Do
* overhaul to arg parse
