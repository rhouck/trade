from parse_rest.datatypes import Object
from parse_rest.user import User as ParseUser
import datetime
from random import choice
import string
from django.utils.timezone import utc
from settings import LIVE

class Company(Object):
    pass
class CashLedger(Object):
    pass


def gen_alphanum_key():
    key = ''
    for i in range(8):
        key += choice(string.uppercase + string.lowercase + string.digits)
    return key

def get_company_by_ticker(ticker):
	"""
	finds company in parse db matching ticker
	"""
	if not isinstance(ticker, str):
		raise ValueError('ticker must be string.')
	company = Company.Query.get(ticker=ticker)
	return company


def offer(user_id, dir, quant, px=None):
	"""
	use this function to offer to buy or sell shares
	user_id - parse user id
	dir - str 'buy' or 'sell'
	quant - int num shares
	px - None if market, float if limit
	"""
	pass

def create_parse_user(email, username, password):
	"""
	creates new user object in parse db
	"""

	if not isinstance(username, str) or not isinstance(email, str) or not isinstance(password, str):
		raise ValueError('username, email, and password must be strings.')

	email = email.lower()
	ref = gen_alphanum_key()
	
	user = ParseUser.signup(username=username, password=password, email=email, ref=ref)
	return user	

def update_cash_ledger(user_id, amount):
	"""
	records changes to cash balance due to trades, signups, referrals, etc
	user_id - parse user id
	amount - float representing dollar value
	"""

	if not isinstance(user_id, unicode):
		raise ValueError('user_id must be unicode.')
	if not isinstance(amount, float):
		raise ValueError('amount must be float.')
	
	cash_ledger_item = CashLedger(user_id=user_id, amount=amount)
	cash_ledger_item.save()
	return cash_ledger_item

def user_signup(email, username, password):
	"""
	call functions required to setup new user
	"""

	if not isinstance(username, str) or not isinstance(email, str) or not isinstance(password, str):
		raise ValueError('username, email, and password must be strings.')

	try:
		user = create_parse_user(email, username, password)
	except Exception as err:
		raise Exception(err)

	try:
		update_cash_ledger(user.objectId, 100.0)
	except Exception as err:
		# delete created user if error in update_cash_ledger
		user.delete()
		raise Exception(err)

	return user

if __name__ == "__main__":
	
	from settings import PARSE_CONFIG
	from parse_rest.connection import register
	register(PARSE_CONFIG['app_id'], PARSE_CONFIG['api_key'])
	