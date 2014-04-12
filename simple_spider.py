import requests
from bs4 import BeautifulSoup
import sys
from datetime import date

def get_all_pages_for_domain(domain_url):
	"""Returns a list of URLs extracted from the sitemap xml"""
	sitemap = requests.get(domain_url + "/sitemap.xml")
	xml = BeautifulSoup(sitemap.content, 'xml')
	links = []
	for link in xml.findAll('loc'):
		links.append(link.string.encode('ascii','ignore'))
	return links

def extract_links_from_html(parent_url):
	"""Returns a list of unique URLs extracted from a page"""
	parent_page = requests.get(parent_url)
	html = BeautifulSoup(parent_page.content, 'lxml')
	links = {}
	for link in html.findAll('a'):
		links[link.get('href').encode('ascii','ignore')] = parent_url
	return links

def inspect_links(urls):
	"""Returns a dictionary of bad links with their status codes"""
	results = {}
	for url in urls:
		try:
			request = requests.get(url)
		except Exception, e:
			results[url] = {"status" : str(e), "parent_page" : urls[url]}
			pass
		if request.status_code != 200:
			results[url] = {"status" : str(request.status_code), "parent_page" : urls[url]}
	return results

def print_report(errors, domain):
	print "Bad URLs for " + domain
	for error in errors:
		print "bad url: " + error
		print "status: " + errors[error]['status']
		print "parent page: " + errors[error]['parent_page']
		print ""

def html_report(errors, domain):
	try:
		f = open("spider.html", "w")
		f.write("<html><head><title>spider report " + str(date.today()) + "</title></head></body>")
		f.write("<h3>Bad URLs for " + domain + " for " + str(date.today()) +"</h3>")
		for error in errors:
			f.write("<p>bad url: " + error + "<br>")
			f.write("status: " + errors[error]['status'] + "<br>")
			f.write("parent page: " + errors[error]['parent_page'] + "<br>")
			f.write("</p>");
		f.write("</body></html>")
	finally:
		f.close()

def main(argv):
	if len(argv) != 2:
		print "Usage: python simple_spider.py http://www.sampledomain.com"
	else:
		domain = argv[1]
		all_pages = get_alL_pages_for_domain(domain)
		all_links = {}
		for page in all_pages:
			all_links.update(extract_links_from_html(page))
		all_links.pop('', None)
		errors = inspect_links(all_links)
		print_report(errors, domain)
		html_report(errors, domain)

if __name__ == "__main__":
    main(sys.argv)
