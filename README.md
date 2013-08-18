Spider
======
A spider that relies on google sitemap.xml to look for broken links in your site.

### Setup
```
sudo easy_install requests

sudo easy_install beautifulsoup4 

sudo easy_install lxml

sudo easy_install mox

sudo easy_install requests_testadapter
```

### To Do
* use list of site pages to collect all links across the domain
* enforce uniqueness in the collection of all links
* format urls to they are uniform
* hit all links in sanitized list
* generate an email report based on the spider results
* exclude spider from analytics
