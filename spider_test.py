import unittest
import mox
from requests_testadapter import TestAdapter
from spider import *


class TestSpider(unittest.TestCase):
	def setUp(self):
		self.sitemap_xml = open("test_files/sitemap.xml","r").read()
		
		self.session = requests.Session()
		
		self.mock = mox.Mox()
		self.mock.StubOutWithMock(requests, 'get')

		
	def test_get_alL_pages_for_domain(self):
		#make a test request object
		self.session.mount('http://', TestAdapter(self.sitemap_xml, status=200))
		
		#when the user asks for devlogged.com, return test request object
		requests.get(mox.IgnoreArg()).AndReturn(self.session.get('http://www.devlogged.com'))
		self.mock.ReplayAll()
		
		#see of the test request object is parsed as expect
		links = ["http://www.devlogged.com/about/", "http://www.devlogged.com/tools/"]
		self.assertEqual(links, get_alL_pages_for_domain('http://www.devlogged.com'))
	
unittest.main()
