from django.test import TestCase
import os
from trade.settings import *
from trade.utils import *


class BuyIPOSharesTests(TestCase):
	
	def setUp(self):
		
		register(PARSE_CONFIG_DEV['app_id'], PARSE_CONFIG_DEV['api_key'])

		# company
		self.name = "TestCo"
		self.ticker = "TST"

		# user 
		self.username = 'username'
		self.password = 'password'
		self.email = 'test@test.com'
		
		# create test user, company and ipo object
		user = user_signup(self.email, self.username, self.password)
		self.user_id = user.objectId
		create_company(self.name, self.ticker)
		create_ipo_object(self.ticker, 10.0, 100)

	def tearDown(self):
		user = ParseUser.login(self.username, self.password)
		user.delete()

		try:
			ipo = IPO.Query.get(ticker=self.ticker)
			ipo.delete()
		except:
			pass

		company = Company.Query.get(ticker=self.ticker)
		company.delete()


	
	# test expired ipo
	# test insufficient cash
	# test insufficient shares available
	
	def test_purchase_ipo_shares_with_no_ipo(self):
		ipo = IPO.Query.get(ticker=self.ticker)
		ipo.delete()

		raised = False
		try:
			buy_ipo_shares(self.user_id, self.ticker, 10)
		except:
			raised = True
		self.assertTrue(raised, 'Did not properly check that an IPO object was available')

	def test_purchase_ipo_shares_inputs(self):
		"""
		test impropper inputs
		"""
		raised = False
		try:
			buy_ipo_shares(1, self.ticker, 10)
		except:
			raised = True
		self.assertTrue(raised, 'Did not catch impropper user_id value')

		raised = False
		try:
			buy_ipo_shares(self.user_id, 1, 10)
		except:
			raised = True
		self.assertTrue(raised, 'Did not catch impropper ticker value')

		raised = False
		try:
			buy_ipo_shares(self.user_id, self.ticker, '10')
		except:
			raised = True
		self.assertTrue(raised, 'Did not catch impropper quantity value')

