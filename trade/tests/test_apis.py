from django.test import TestCase
import os
from trade.settings import *
from trade.utils import *

class ApiConnectionTests(TestCase):
	"""
	check connections to external apis and services
	"""
	def test_parse_connection_prod(self):
		"""
		confirm propper connection to parse product db
		"""
		# trigger exception if register credentials aren't correct
		raised = False
		try:
			register(PARSE_CONFIG['app_id'], PARSE_CONFIG['api_key'])	
			users = [u for u in ParseUser.Query.all().limit(1)]
		except:
			raised = True
		self.assertFalse(raised, 'Exception raised')

	def test_parse_connection_dev(self):
		"""
		confirm propper connection to parse dev db
		"""
		# trigger exception if register credentials aren't correct
		raised = False
		try:
			register(PARSE_CONFIG_DEV['app_id'], PARSE_CONFIG_DEV['api_key'])	
			users = [u for u in ParseUser.Query.all().limit(1)]
		except:
			raised = True
		self.assertFalse(raised, 'Exception raised')
