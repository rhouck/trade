from django.test import TestCase
import os
from trade.settings import *
from trade.utils import *

from utils import *

class UserSignupTests(TestCase):

	def setUp(self):

		register(PARSE_CONFIG_DEV['app_id'], PARSE_CONFIG_DEV['api_key'])	

		self.email = "test@test.com"
		self.username = "test"
		self.password = "test_password"
		self.user_count = sum([1 for i in ParseUser.Query.all()])
		self.port_count = sum([1 for i in Portfolio.Query.all()])
		self.ledger_count = sum([1 for i in Ledger.Query.all()])

		# create test exchange user
		self.test_exchange_user = create_test_exchange_user()

	def tearDown(self):
		
		drop_test_user(self.username, self.password)

		drop_test_user(self.test_exchange_user['user'].username, self.test_exchange_user['password'])

		# confirm number of user and ledger objects has not changed as a result of testing
		post_user_count = sum([1 for i in ParseUser.Query.all()])
		self.assertEqual(self.user_count, post_user_count)
		
		post_port_count = sum([1 for i in Portfolio.Query.all()])
		self.assertEqual(self.port_count, post_port_count)

		post_ledger_count = sum([1 for i in Ledger.Query.all()])
		self.assertEqual(self.ledger_count, post_ledger_count)


	def test_create_user(self):
		
		"""
		test invalid email
		"""
		raised = raises_exception(user_signup, 'email', self.username, self.password, self.test_exchange_user['user'])
		self.assertTrue(raised, 'Did not recognize bad email format')
		
		"""
		test invalid email value type
		"""		
		raised = raises_exception(user_signup, 1, self.username, self.password, self.test_exchange_user['user'])
		self.assertTrue(raised, 'Did not recognize incorrect email value')

		"""
		test invalid username value type
		"""
		raised = raises_exception(user_signup, self.email, 1, self.password, self.test_exchange_user['user'])
		self.assertTrue(raised, 'Did not recognize incorrect username value')

		"""
		test invalid password value type
		"""
		raised = raises_exception(user_signup, self.email, self.username, 1, self.test_exchange_user['user'])
		self.assertTrue(raised, 'Did not recognize incorrect password value')

		"""
		test invalid exchange user value type
		"""
		raised = raises_exception(user_signup, self.email, self.username, self.password, 'user')
		self.assertTrue(raised, 'Did not recognize incorrect user value')

		"""
		test propper sign up
		"""
		raised = raises_exception(user_signup, self.email, self.username, self.password, self.test_exchange_user['user'])
		self.assertFalse(raised, 'Did not create new user')
	
	
	def test_create_duplicate_user(self):
		"""
		try creating duplicate user
		"""
		user_signup(self.email, self.username, self.password, self.test_exchange_user['user'])
		raised = raises_exception(user_signup, self.email, self.username, self.password, self.test_exchange_user['user'])
		self.assertTrue(raised, 'Created duplicate user')

class CompanyTests(TestCase):
	
	def setUp(self):
		
		register(PARSE_CONFIG_DEV['app_id'], PARSE_CONFIG_DEV['api_key'])

		self.name = "TestCo"
		self.ticker = "TST"

		self.co_count = sum([1 for i in Company.Query.all()])
		
	def tearDown(self):
		company = Company.Query.get(ticker=self.ticker)
		company.delete()

		# confirm number of company objects has not changed as a result of testing
		post_co_count = sum([1 for i in Company.Query.all()])
		self.assertEqual(self.co_count, post_co_count)

	def test_create_company_and_duplicates(self):
		
		"""
		test impropper inputs
		"""
		raised = raises_exception(create_company, 1, self.ticker)
		self.assertTrue(raised, 'Did not catch impropper name value')

		raised = raises_exception(create_company, self.name, 1)
		self.assertTrue(raised, 'Did not catch impropper ticker value')

	
		"""
		test propper company creation
		"""
		raised = raises_exception(create_company, self.name, self.ticker)
		self.assertFalse(raised, 'Could not create test company')

		"""
		test creating duplicate companies
		"""
		raised = raises_exception(create_company, self.name, 'tickertest')
		self.assertTrue(raised, 'Could create duplicate name company')

		raised = raises_exception(create_company, 'nametest', self.ticker)
		self.assertTrue(raised, 'Could create duplicate ticker company')


class IPOTests(TestCase):
	
	def setUp(self):
		
		register(PARSE_CONFIG_DEV['app_id'], PARSE_CONFIG_DEV['api_key'])

		self.name = "TestCo"
		self.ticker = "TST"
		self.price = 10.0
		self.auth = 1000000
		
		self.ipo_count = sum([1 for i in IPO.Query.all()])
	
		self.port_count = sum([1 for i in Portfolio.Query.all()])
		
		# create test company
		create_company(self.name, self.ticker)

		# create test exchange user
		self.test_exchange_user = create_test_exchange_user()

	def tearDown(self):
		
		company = Company.Query.get(ticker=self.ticker)
		company.delete()
		
		drop_test_user(self.test_exchange_user['user'].username, self.test_exchange_user['password'])

		try:
			# certain tests don't result in created IPO item so can't force delete object
			ipo_item = IPO.Query.get(ticker=self.ticker)
			ipo_item.delete()
		except:
			pass

		# confirm number of ipo objects has not changed as a result of testing
		post_ipo_count = sum([1 for i in IPO.Query.all()])
		self.assertEqual(self.ipo_count, post_ipo_count)

		# confirm number of portfolio objects has increased by one
		post_port_count = sum([1 for i in Portfolio.Query.all()])
		self.assertEqual(self.port_count, post_port_count)


	def test_create_ipo_object_where_co_not_exist(self):
		
		raised = raises_exception(create_ipo_object, 'BADTICKER', self.price, self.auth, self.test_exchange_user['user'])
		self.assertTrue(raised, "Created IPO object not tied to existing company")

		# confirm number of portfolio objects has increased by one
		post_port_count = sum([1 for i in Portfolio.Query.all()])
		self.assertEqual(self.port_count, post_port_count-1)
	
	def test_create_ipo_object(self):
		"""
		test impropper inputs
		"""
		raised = raises_exception(create_ipo_object, 1, self.price, self.auth, self.test_exchange_user['user'])
		self.assertTrue(raised, 'Did not catch impropper ticker value')

		raised = raises_exception(create_ipo_object, self.ticker, 'price', self.auth, self.test_exchange_user['user'])
		self.assertTrue(raised, 'Did not catch impropper price value')

		raised = raises_exception(create_ipo_object, self.ticker, self.price, 'auth', self.test_exchange_user['user'])
		self.assertTrue(raised, 'Did not catch impropper auth value')

		raised = raises_exception(create_ipo_object, self.ticker, self.price, self.auth, 'user')
		self.assertTrue(raised, 'Did not catch impropper exchange user value')

		"""
		test propper ipo creation
		"""		
		raised = raises_exception(create_ipo_object, self.ticker, self.price, self.auth, self.test_exchange_user['user'])
		self.assertFalse(raised, 'Could not create test IPO')

		# confirm number of portfolio objects has increased by one
		post_port_count = sum([1 for i in Portfolio.Query.all()])
		self.assertEqual(self.port_count, post_port_count-2)
		
		# confirm latest portfolio object for excahnge reflects ipo
		current_exchange_portfolio = Portfolio.Query.filter(user_id=self.test_exchange_user['user'].objectId).order_by("-createdAt").limit(1)[0]
		self.assertEqual(getattr(current_exchange_portfolio, self.ticker), self.auth)


	def test_creation_of_duplicate_ipo_objects(self):
		"""
		test creating duplicate ipo objects
		"""
		create_ipo_object(self.ticker, self.price, self.auth, self.test_exchange_user['user'])
		raised = raises_exception(create_ipo_object, self.ticker, self.price, self.auth, self.test_exchange_user['user'])
		self.assertTrue(raised, 'Could create duplicate name company')

		# confirm number of portfolio objects has increased by one
		post_port_count = sum([1 for i in Portfolio.Query.all()])
		self.assertEqual(self.port_count, post_port_count-2)

class LedgerTests(TestCase):
	pass