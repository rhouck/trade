from trade.settings import *
from trade.utils import *
from parse_rest.connection import ParseBatcher


def raises_exception(func, *args, **kwargs):
	"""
	pass functions with parameters here to test whether they raise exceptions
	"""
	raised = False
	try:
		func(*args, **kwargs)
	except Exception as err:
		#print "Error message: %s" % (err)
		raised = True
	return raised

def drop_test_user(username, password):
	"""
	delete user and associated portfolio and ledger objects
	"""
	
	batcher = ParseBatcher()

	user = ParseUser.login(username, password)
		
	port_items = Portfolio.Query.filter(user_id=user.objectId)
	batcher.batch_delete(port_items)
	
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