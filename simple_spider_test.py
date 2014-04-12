import unittest
import mox
from requests_testadapter import TestAdapter
from simple_spider import *


class TestSpider(unittest.TestCase):

	def setUp(self):
		self.page = open("test_files/sample_page.html", "r").read()
		self.session = requests.Session()
		self.mock = mox.Mox()
		self.mock.StubOutWithMock(requests, 'get')

	def tearDown(self):
		self.mock.UnsetStubs()

	def test_get_alL_pages_for_domain(self):
		sitemap_xml = open("test_files/sitemap.xml","r").read()
		self.session.mount('http://www.devlogged.com', TestAdapter(sitemap_xml, status=200))
		requests.get(mox.IgnoreArg()).AndReturn(self.session.get('http://www.devlogged.com'))
		self.mock.ReplayAll()

		links = ['http://www.devlogged.com/about/', 'http://www.devlogged.com/tools/']
		self.assertEqual(links, get_all_pages_for_domain('http://www.devlogged.com'))

	def test_extract_links_from_html(self):
		self.session.mount('http://www.devlogged.com/about', TestAdapter(self.page, status=200))
		requests.get(mox.IgnoreArg()).AndReturn(self.session.get('http://www.devlogged.com/about'))
		self.mock.ReplayAll()

		links = {'http://wordpress.com' : 'http://www.devlogged.com/about', 'http://aws.amazon.com/ec2/' : 'http://www.devlogged.com/about'}
		extracted_links = extract_links_from_html('http://www.devlogged.com/about')
		self.assertEqual(links, extracted_links)
		self.assertEqual(2, len(extracted_links))

	def test_inspect_links(self):
		self.session.mount('http://wordpress.com', TestAdapter(self.page, status=200))
		self.session.mount('http://aws.amazon.com/ec2/', TestAdapter(self.page, status=404))
		requests.get('http://wordpress.com').AndReturn(self.session.get('http://wordpress.com'))
		requests.get('http://aws.amazon.com/ec2/').AndReturn(self.session.get('http://aws.amazon.com/ec2/'))
		self.mock.ReplayAll()

		urls = {'http://wordpress.com' : 'found', 'http://aws.amazon.com/ec2/' : 'found'}
		bad_links = {'http://aws.amazon.com/ec2/' : {'status': '404', 'parent_page': 'found'}}
		self.assertEquals(bad_links, inspect_links(urls))

unittest.main()
