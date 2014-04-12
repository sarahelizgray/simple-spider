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

def extract_links_from_page_content(parent_url):
	"""Returns a list of unique URLs extracted from a page"""
	parent_page = requests.get(parent_url)
	html = BeautifulSoup(parent_page.content, 'lxml')
	links = {}
	for link in html.findAll('a'):
		links[link.get('href').encode('ascii','ignore')] = parent_url
	return links

def inspect_links(urls, verbose=False):
	"""Returns a dictionary of bad links with their status codes"""
	results = {}
	for url in urls:
		if verbose: print "inspecting " + url
		try:
			request = requests.get(url)
		except Exception, e:
			results[url] = {"status" : str(e), "parent_page" : urls[url]}
			pass
		if request.status_code != 200:
			bad_url_details = {"status" : str(request.status_code), "parent_page" : urls[url]}
			if verbose: print bad_url_details
			results[url] = bad_url_details
	return results

def print_report(errors, domain):
	print "Bad URLs for " + domain
	for error in errors:
		print "bad url: " + error
		print "status: " + errors[error]['status']
		print "parent page: " + errors[error]['parent_page']
		print ""

def html_report(bad_urls, domain):
	try:
		f = open("spider.html", "w")
		f.write("<html>")
		f.write("<head><title>spider report " + str(date.today()) + "</title></head>")
		f.write("<body>")
		f.write("<h3>Bad URLs for " + domain + " for " + str(date.today()) +"</h3>")
		for bad_url in bad_urls:
			f.write("<p>bad url: " + bad_url + "<br>")
			f.write("status: " + bad_urls[bad_url]['status'] + "<br>")
			f.write("parent page: " + bad_urls[bad_url]['parent_page'] + "<br>")
			f.write("</p>");
		f.write("</body>")
		f.write("</html>")
	finally:
		f.close()

def set_verbose_output(print_to_stdout):
	if print_to_stdout == "--verbose":
		verbose = True
	else:
		verbose = False
	return verbose

def main(argv):
	verbose = False
	if len(argv) < 2:
		print "Usage: python simple_spider.py http://www.sampledomain.com <--verbose>"
	else:
		domain = argv[1]
		if len(argv) > 2: verbose = set_verbose_output(argv[2])
		all_pages = get_all_pages_for_domain(domain)
		all_links = {}
		for page in all_pages:
			all_links.update(extract_links_from_page_content(page))
		all_links.pop('', None)
		errors = inspect_links(all_links, verbose)
		html_report(errors, domain)

		if verbose:
			print_report(errors, domain)

if __name__ == "__main__":
    main(sys.argv)
