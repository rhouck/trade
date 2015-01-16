from trade.settings import *
from trade.utils import *

def drop_test_user(username, password):
	"""
	delete user and associated portfolio and ledger objects
	"""
	user = ParseUser.login(username, password)
		
	port_item = Portfolio.Query.get(user_id=user.objectId)
	port_item.delete()

	ledger_item = Ledger.Query.get(user_id=user.objectId)
	ledger_item.delete()

	user.delete()