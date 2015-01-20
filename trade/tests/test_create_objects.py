from django.test import TestCase
import os
from trade.settings import *
from trade.utils import *
import random

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
	
	def setUp(self):
		
		register(PARSE_CONFIG_DEV['app_id'], PARSE_CONFIG_DEV['api_key'])

		self.ledger_count = sum([1 for i in Ledger.Query.all()])

		# create test exchange user
		self.test_exchange_user = create_test_exchange_user()
		
		self.ticker = 'TST'
		self.share_price = 1.0
		self.share_quantity = 3
		self.amount = self.share_quantity * self.share_price 
		self.fees = FEE_RATE * self.amount

		# create test users
		self.test_user_passwords = 'password'
		self.test_user_1 = user_signup('test1@user.com', 'test_user_1', self.test_user_passwords, self.test_exchange_user['user'])
		self.test_user_2 = user_signup('test2@user.com', 'test_user_2', self.test_user_passwords, self.test_exchange_user['user'])

		# setup user portfolios
		update_portfolio_object(self.test_user_1.objectId, {'TST': 10})

	def tearDown(self):

		drop_test_user(self.test_user_1.username, self.test_user_passwords)
		drop_test_user(self.test_user_2.username, self.test_user_passwords)

		drop_test_user(self.test_exchange_user['user'].username, self.test_exchange_user['password'])

		post_ledger_count = sum([1 for i in Ledger.Query.all()])
		self.assertEqual(self.ledger_count, post_ledger_count)

	def test_impropper_ledger_inputs(self):
		
		raised = raises_exception(update_ledger, 1, self.test_user_2.objectId, self.amount, ticker=self.ticker, share_price=self.share_price, share_quantity=self.share_quantity, fees=self.fees)
		self.assertTrue(raised, "Did not recognize impropper from_user_id inputs.")

		raised = raises_exception(update_ledger, self.test_user_1.objectId, 1, self.amount, ticker=self.ticker, share_price=self.share_price, share_quantity=self.share_quantity, fees=self.fees)
		self.assertTrue(raised, "Did not recognize impropper to_user_id inputs.")

		raised = raises_exception(update_ledger, self.test_user_1.objectId, self.test_user_1.objectId, self.amount, ticker=self.ticker, share_price=self.share_price, share_quantity=self.share_quantity, fees=self.fees)
		self.assertTrue(raised, "Did not recognize from and to user ids must be different.")

		raised = raises_exception(update_ledger, self.test_user_1.objectId, self.test_user_2.objectId, 'amount', ticker=self.ticker, share_price=self.share_price, share_quantity=self.share_quantity, fees=self.fees)
		self.assertTrue(raised, "Did not recognize impropper amount inputs.")

		raised = raises_exception(update_ledger, self.test_user_1.objectId, self.test_user_2.objectId, 0, ticker=self.ticker, share_price=self.share_price, share_quantity=self.share_quantity, fees=self.fees)
		self.assertTrue(raised, "Did not recognize impropper amount most be positive number.")
	

		raised = raises_exception(update_ledger, self.test_user_1.objectId, self.test_user_2.objectId, self.amount, ticker=1.0, share_price=self.share_price, share_quantity=self.share_quantity, fees=self.fees)
		self.assertTrue(raised, "Did not require ticker to be string.")

		raised = raises_exception(update_ledger, self.test_user_1.objectId, self.test_user_2.objectId, self.amount, ticker=self.ticker, share_price='share price', share_quantity=self.share_quantity, fees=self.fees)
		self.assertTrue(raised, "Did not require share_price to be float.")

		raised = raises_exception(update_ledger, self.test_user_1.objectId, self.test_user_2.objectId, self.amount, ticker=self.ticker, share_price=self.share_price, share_quantity=1.23, fees=self.fees)
		self.assertTrue(raised, "Did not require share_qunatity to be int.")

		raised = raises_exception(update_ledger, self.test_user_1.objectId, self.test_user_2.objectId, self.amount, ticker=self.ticker, share_price=self.share_price, share_quantity=self.share_quantity, fees='fees')
		self.assertTrue(raised, "Did not require fees to be float.")

		# confirm that if any of the share purchase items are provided, they all must be provided
		purchase_cols = [self.ticker, self.share_price, self.share_quantity, self.fees]
		choice = random.randint(0,len(purchase_cols)-1)
		purchase_cols[choice] = None
		raised = raises_exception(update_ledger, self.test_user_1.objectId, self.test_user_2.objectId, self.amount, ticker=purchase_cols[0], share_price=purchase_cols[1], share_quantity=purchase_cols[2], fees=purchase_cols[3])
		self.assertTrue(raised, "Did not ensure that all share purchase values are provided if any are provided.")

		post_ledger_count = sum([1 for i in Ledger.Query.all()])
		self.assertEqual(self.ledger_count, post_ledger_count-2)

	def test_proper_cash_transfer(self):
		
		raised = raises_exception(update_ledger, self.test_user_1.objectId, self.test_user_2.objectId, self.amount)
		self.assertFalse(raised, "Didn't enable transfer of cash or value without tie to share sale.")	

		post_ledger_count = sum([1 for i in Ledger.Query.all()])
		self.assertEqual(self.ledger_count, post_ledger_count-3)

	def test_proper_share_purchase(self):
		
		raised = raises_exception(update_ledger, self.test_user_1.objectId, self.test_user_2.objectId, self.amount, ticker=self.ticker, share_price=self.share_price, share_quantity=self.share_quantity, fees=self.fees)
		self.assertFalse(raised, "Didn't properly create share transfer ledger item.")	

		post_ledger_count = sum([1 for i in Ledger.Query.all()])
		self.assertEqual(self.ledger_count, post_ledger_count-3)

		
		