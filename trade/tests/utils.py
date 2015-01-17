from trade.settings import *
from trade.utils import *
from parse_rest.connection import ParseBatcher

def drop_test_user(username, password):
	"""
	delete user and associated portfolio and ledger objects
	"""
	
	batcher = ParseBatcher()

	user = ParseUser.login(username, password)
		
	#port_item = Portfolio.Query.get(user_id=user.objectId)
	#port_item.delete()

	port_items = Portfolio.Query.filter(user_id=user.objectId)
	batcher.batch_delete(port_items)
	
	#ledger_item = Ledger.Query.get(user_id=user.objectId)
	#ledger_item.delete()

	ledger_items = Ledger.Query.filter(to_user_id=user.objectId)
	batcher.batch_delete(ledger_items)

	ledger_items = Ledger.Query.filter(from_user_id=user.objectId)
	batcher.batch_delete(ledger_items)

	user.delete()

def create_test_exchange_user():

	password = 'password'

	user = ParseUser.signup(username='TestExchange', password=password, email='test@email.com')
	user.save()

	port_item = Portfolio(user_id=user.objectId, cash_balance=0.0)
	port_item.save()

	return {'user': user, 'password': password}