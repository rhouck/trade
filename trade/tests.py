from django.test import TestCase
import os
from settings import *
from utils import *

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


class UserSignupTests(TestCase):

	def setUp(self):

		register(PARSE_CONFIG_DEV['app_id'], PARSE_CONFIG_DEV['api_key'])	

		self.email = "test@test.com"
		self.username = "test"
		self.password = "test_password"
		self.user_count = sum([1 for i in ParseUser.Query.all()])
		self.port_count = sum([1 for i in Portfolio.Query.all()])
		self.ledger_count = sum([1 for i in Ledger.Query.all()])

	def tearDown(self):
		"""
		delete test user from db
		"""
		user = ParseUser.login(self.username, self.password)
		
		port_item = Portfolio.Query.get(user_id=user.objectId)
		port_item.delete()

		ledger_item = Ledger.Query.get(user_id=user.objectId)
		ledger_item.delete()
		
		user.delete()

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
		raised = False
		try:
			user_signup('email', self.username, self.password)
		except:
			raised = True
		self.assertTrue(raised, 'Did not recognize bad email format')
		
		"""
		test invalid email value type
		"""		
		raised = False
		try:
			user_signup(1, self.username, self.password)
		except:
			raised = True
		self.assertTrue(raised, 'Did not recognize incorrect email value')

		"""
		test invalid username value type
		"""
		raised = False
		try:
			user_signup(self.email, 1, self.password)
		except:
			raised = True
		self.assertTrue(raised, 'Did not recognize incorrect username value')

		"""
		test invalid password value type
		"""
		raised = False
		try:
			user_signup(self.email, self.username, 1)
		except:
			raised = True
		self.assertTrue(raised, 'Did not recognize incorrect password value')


		"""
		test propper sign up
		"""
		raised = False
		try:
			user_signup(self.email, self.username, self.password)
		except:
			raised = True
		self.assertFalse(raised, 'Did not create new user')


	def test_create_duplicate_user(self):
		"""
		try creating duplicate user
		"""
		raised = False
		try:
			user_signup(self.email, self.username, self.password)
			user_signup(self.email, self.username, self.password)
		except:
			raised = True
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
		raised = False
		try:
			create_company(1, self.ticker)
		except:
			raised = True
		self.assertTrue(raised, 'Did not catch impropper name value')

		raised = False
		try:
			create_company(self.name, 1)
		except:
			raised = True
		self.assertTrue(raised, 'Did not catch impropper ticker value')

	
		"""
		test propper company creation
		"""
		raised = False
		try:
			create_company(self.name, self.ticker)
		except:
			raised = True
		self.assertFalse(raised, 'Could not create test company')

		"""
		test creating duplicate companies
		"""
		raised = False
		try:
			create_company(self.name, 'tickertest')
		except:
			raised = True
		self.assertTrue(raised, 'Could create duplicate name company')

		raised = False
		try:
			create_company('nametest', self.ticker)
		except:
			raised = True
		self.assertTrue(raised, 'Could create duplicate ticker company')


class IPOTests(TestCase):
	
	def setUp(self):
		
		register(PARSE_CONFIG_DEV['app_id'], PARSE_CONFIG_DEV['api_key'])

		self.name = "TestCo"
		self.ticker = "TST"
		self.price = 10.0
		self.auth = 1000000
		
		self.ipo_count = sum([1 for i in IPO.Query.all()])

		# create test company
		create_company(self.name, self.ticker)
	
	def tearDown(self):
		
		company = Company.Query.get(ticker=self.ticker)
		company.delete()

		try:
			# certain tests don't result in created IPO item so can't force delete object
			ipo_item = IPO.Query.get(ticker=self.ticker)
			ipo_item.delete()
		except:
			pass

		# confirm number of ipo objects has not changed as a result of testing
		post_ipo_count = sum([1 for i in IPO.Query.all()])
		self.assertEqual(self.ipo_count, post_ipo_count)

	
	def test_create_ipo_object_where_co_not_exist(self):
		raised = False
		try:
			create_ipo_object('BADTICKER', self.price, self.auth)
		except:
			raised = True
		self.assertTrue(raised, "Created IPO object not tied to existing company")
	
	def test_create_ipo_object(self):

		"""
		test impropper inputs
		"""
		raised = False
		try:
			create_ipo_object(1, self.price, self.auth)
		except:
			raised = True
		self.assertTrue(raised, 'Did not catch impropper ticker value')

		raised = False
		try:
			create_ipo_object(self.ticker, 'price', self.auth)
		except:
			raised = True
		self.assertTrue(raised, 'Did not catch impropper price value')

		raised = False
		try:
			create_ipo_object(self.ticker, self.price, 'auth')
		except:
			raised = True
		self.assertTrue(raised, 'Did not catch impropper auth value')

	
		"""
		test propper ipo creation
		"""
		raised = False
		try:
			create_ipo_object(self.ticker, self.price, self.auth)
		except Exception as err:
			print err
			raised = True
		self.assertFalse(raised, 'Could not create test IPO')

	def test_creation_of_duplicate_ipo_objects(self):
		"""
		test creating duplicate ipo objects
		"""
		raised = False
		try:
			create_ipo_object(self.ticker, self.price, self.auth)
			create_ipo_object(self.ticker, self.price, self.auth)
		except:
			raised = True
		self.assertTrue(raised, 'Could create duplicate name company')

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


	# test no ipo object
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

