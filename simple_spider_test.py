import unittest
import mox
from requests_testadapter import TestAdapter
from simple_spider import *


class TestSpider(unittest.TestCase):
	def setUp(self):
		self.sitemap_xml = open("test_files/sitemap.xml","r").read()
		self.page = open("test_files/sample_page.html", "r").read()
		
		self.session = requests.Session()
		
		self.mock = mox.Mox()
		self.mock.StubOutWithMock(requests, 'get')
		
	def tearDown(self):
		self.mock.UnsetStubs()
		
	def test_get_alL_pages_for_domain(self):
		self.session.mount('http://', TestAdapter(self.sitemap_xml, status=200))
		requests.get(mox.IgnoreArg()).AndReturn(self.session.get('http://www.devlogged.com'))
		self.mock.ReplayAll()
		
		links = ["http://www.devlogged.com/about/", "http://www.devlogged.com/tools/"]
		self.assertEqual(links, get_alL_pages_for_domain('http://www.devlogged.com'))
	
	def test_extract_links_from_html(self):
		self.session.mount('http://', TestAdapter(self.page, status=200))
		requests.get(mox.IgnoreArg()).AndReturn(self.session.get('http://www.devlogged.com/about'))
		self.mock.ReplayAll()
		
		links = {"http://wordpress.com" : "found", "http://aws.amazon.com/ec2/" : "found"}
		extracted_links = extract_links_from_html('http://www.devlogged.com/about')
		self.assertEqual(links, extracted_links)
		self.assertEqual(2, len(extracted_links))
		
		
unittest.main()
