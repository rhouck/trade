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


from parse_rest.user import User as ParseUser

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
		self.user_count = sum([i for i in ParseUser.Query.all()])
		self.ledger_count = sum([i for i in CashLedger.Query.all()])

	def tearDown(self):
		"""
		delete test user from db
		"""
		user = ParseUser.login(self.username, self.password)
		cash_ledger_item = CashLedger.Query.get(user_id=user.objectId)
		cash_ledger_item.delete()
		user.delete()

		# confirm number of user and cash ledger objects has not changed as a result of testing
		post_user_count = sum([i for i in ParseUser.Query.all()])
		self.assertEqual(self.user_count, post_user_count)
		
		post_ledger_count = sum([i for i in CashLedger.Query.all()])
		self.assertEqual(self.ledger_count, post_ledger_count)

	
	def test_create_user(self):
		
		"""
		test invalid email
		"""
		email = 'email'
		raised = False
		try:
			user_signup(email, self.username, self.password)
		except:
			raised = True
		self.assertTrue(raised, 'Did not recognize bad email format')
		
		"""
		test invalid email value type
		"""		
		email = 1
		raised = False
		try:
			user_signup(email, self.username, self.password)
		except:
			raised = True
		self.assertTrue(raised, 'Did not recognize incorrect email value')

		"""
		test invalid username value type
		"""
		username = 1
		raised = False
		try:
			user_signup(self.email, username, self.password)
		except:
			raised = True
		self.assertTrue(raised, 'Did not recognize incorrect username value')

		"""
		test invalid password value type
		"""
		password = 1
		raised = False
		try:
			user_signup(self.email, self.username, password)
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



