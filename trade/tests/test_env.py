from django.test import TestCase
import os
from trade.settings import *

class EnvVarsTests(TestCase):
	"""
	check environment settings are available
	"""
	def test_django_secret_key_available(self):
		"""
		confirm configuration variables are available
		"""
		self.assertTrue(SECRET_KEY)

	def test_parse_configuration_vars_are_available(self):
		"""
		confirm configuration variables are available
		"""
		self.assertTrue(PARSE_CONFIG['app_id'])
		self.assertTrue(PARSE_CONFIG['api_key'])

		self.assertTrue(PARSE_CONFIG_DEV['app_id'])
		self.assertTrue(PARSE_CONFIG_DEV['api_key'])

	def test_parse_exchange_user_vars_are_available(self):
		"""
		confirm configuration variables are available
		"""
		self.assertTrue(EXCHANGE_USER_CONFIG['email'])
		self.assertTrue(EXCHANGE_USER_CONFIG['username'])
		self.assertTrue(EXCHANGE_USER_CONFIG['password'])
		
