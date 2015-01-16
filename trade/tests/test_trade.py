from django.test import TestCase
import os
from trade.settings import *
from trade.utils import *

class ExchangeUserTests(TestCase):

	def test_find_object(self):
		
		self.assertTrue(ExchangeUser, 'Did not find exchange user object')

		raised = False
		try:
			user = Portfolio.Query.get(user_id=ExchangeUser.objectId)
		except:
			raised = True
		self.assertFalse(raised, 'Did not find portfolio object for exhange user')

