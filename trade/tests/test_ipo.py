from django.test import TestCase
import os
from trade.settings import *
from trade.utils import *

from utils import *

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
		
		# create test exchange user
		self.test_exchange_user = create_test_exchange_user()

		# create test user, company and ipo object
		user = user_signup(self.email, self.username, self.password, self.test_exchange_user['user'])
		self.user_id = user.objectId
		create_company(self.name, self.ticker)
		create_ipo_object(self.ticker, 10.0, 100, self.test_exchange_user['user'])

	def tearDown(self):
		
		drop_test_user(self.username, self.password)

		drop_test_user(self.test_exchange_user['user'].username, self.test_exchange_user['password'])

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

		raised = raises_exception(buy_ipo_shares, self.user_id, self.ticker, 10)
		self.assertTrue(raised, 'Did not properly check that an IPO object was available')

	def test_purchase_ipo_shares_inputs(self):
		"""
		test impropper inputs
		"""
		raised = raises_exception(buy_ipo_shares, 1, self.ticker, 10)
		self.assertTrue(raised, 'Did not catch impropper user_id value')

		raised = raises_exception(buy_ipo_shares, self.user_id, 1, 10)
		self.assertTrue(raised, 'Did not catch impropper ticker value')

		raised = raises_exception(buy_ipo_shares, self.user_id, self.ticker, '10')
		self.assertTrue(raised, 'Did not catch impropper quantity value')

