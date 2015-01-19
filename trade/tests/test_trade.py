from django.test import TestCase
import os
from trade.settings import *
from trade.utils import *
from utils import *

class ExchangeUserTests(TestCase):

	def test_find_object(self):
		
		self.assertTrue(ExchangeUser, 'Did not find exchange user object')

	def test_find_object_portfolio(self):

		raised = raises_exception(Portfolio.Query.get, user_id=ExchangeUser.objectId)	
		self.assertFalse(raised, 'Did not find portfolio object for exhange user')

