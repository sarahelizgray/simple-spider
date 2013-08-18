import requests
from bs4 import BeautifulSoup

def get_alL_pages_for_domain(url):
	"""Returns a list of URLs extracted from the sitemap xml"""
	site_request = requests.get(url + "/sitemap.xml")
	site_content = site_request.content
	xml = BeautifulSoup(site_content, 'xml')
	links = []
	for link in xml.findAll('loc'):
		links.append(link.string.encode('ascii','ignore'))
	return links

def extract_links_from_html(url):
	"""Returns a list of unique URLs extracted from a page"""
	site_request = requests.get(url)
	site_html = site_request.content
	html_text = BeautifulSoup(site_html, 'lxml')
	links = {}
	for link in html_text.findAll('a'):
		links[link.get('href')] = "found"
	return links

def inspect_links(urls):	
	"""Returns a dictionary of bad links with their status codes"""
	results = {}
	for url in urls:
		request = requests.get(url)
		if request.status_code != 200:
			results[url] = str(request.status_code)
	return results
		