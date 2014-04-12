import unittest
import mox
from requests_testadapter import TestAdapter
from simple_spider import *
import os
from freezegun import freeze_time


class TestSpider(unittest.TestCase):

	def setUp(self):
		self.page = open("test_files/sample_page.html", "r").read()
		self.session = requests.Session()
		self.mock = mox.Mox()
		self.mock.StubOutWithMock(requests, 'get')
		self.urls_with_parents = {'http://wordpress.com' : 'http://www.devlogged.com/about', 'http://aws.amazon.com/ec2/' : 'http://www.devlogged.com/about'}
		self.bad_url_report = {'http://aws.amazon.com/ec2/' : {'status': '404', 'parent_page': 'http://www.devlogged.com/about'}}
		self.domain = 'http://www.devlogged.com'

	def tearDown(self):
		self.mock.UnsetStubs()

	def test_get_all_pages_for_domain(self):
		sitemap_xml = open("test_files/sitemap.xml","r").read()
		self.session.mount(self.domain, TestAdapter(sitemap_xml, status=200))
		requests.get(mox.IgnoreArg()).AndReturn(self.session.get(self.domain))
		self.mock.ReplayAll()

		links = ['http://www.devlogged.com/about/', 'http://www.devlogged.com/tools/']
		self.assertEqual(links, get_all_pages_for_domain(self.domain))

	def test_extract_links_from_page_content(self):
		page_under_test = 'http://www.devlogged.com/about'
		self.session.mount(page_under_test, TestAdapter(self.page, status=200))
		requests.get(mox.IgnoreArg()).AndReturn(self.session.get(page_under_test))
		self.mock.ReplayAll()

		extracted_urls = extract_links_from_page_content(page_under_test)
		self.assertEqual(self.urls_with_parents, extracted_urls)
		self.assertEqual(2, len(extracted_urls))

	def test_inspect_links(self):
		self.session.mount('http://wordpress.com', TestAdapter(self.page, status=200))
		self.session.mount('http://aws.amazon.com/ec2/', TestAdapter(self.page, status=404))
		requests.get('http://wordpress.com').AndReturn(self.session.get('http://wordpress.com'))
		requests.get('http://aws.amazon.com/ec2/').AndReturn(self.session.get('http://aws.amazon.com/ec2/'))
		self.mock.ReplayAll()

		self.assertEquals(self.bad_url_report, inspect_links(self.urls_with_parents))

	@freeze_time("2014-04-12")
	def test_html_report(self):
		html_report(self.bad_url_report, self.domain)
		generated_spider_report = open("spider.html", "r")
		expected_spider_report = open("test_files/sample_spider_report.html", "r")
		self.assertEquals(expected_spider_report.read(), generated_spider_report.read())
		expected_spider_report.close()
		generated_spider_report.close()
		os.remove("spider.html")

unittest.main()
