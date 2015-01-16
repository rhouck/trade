from django.test import TestCase
import os
from trade.settings import *
from trade.utils import *

class ExchangeUserTests(TestCase):

	def test_find_object(self):
		raised = False
		try:
			user = ParseUser.Query.get(username=EXCHANGE_USER_CONFIG['username'])
		except:
			raised = True
		self.assertFalse(raised, 'Did not find exchange user object')

		raised = False
		try:
			user = Portfolio.Query.get(user_id=user.objectId)
		except:
			raised = True
		self.assertFalse(raised, 'Did not find portfolio object for exhange user')

