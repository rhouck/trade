from parse_rest.datatypes import Object
from parse_rest.user import User as ParseUser
import datetime
from random import choice
import string
from django.utils.timezone import utc
from settings import LIVE, EXCHANGE_USER_CONFIG

class Company(Object):
    pass
class Ledger(Object):
    pass
class IPO(Object):
    pass
class Portfolio(Object):
    pass

def gen_alphanum_key():
    key = ''
    for i in range(8):
        key += choice(string.uppercase + string.lowercase + string.digits)
    return key

# exchange parse user object
def get_exchange_user():
	try:
		return ParseUser.Query.get(username=EXCHANGE_USER_CONFIG['username'])
	except:
		return None
ExchangeUser = get_exchange_user()

def create_portfolio(user_id):
	"""
	creates a portoflio object to periodically summarize cash balance and shares held
	user_id - parse user id
	"""

	if not isinstance(user_id, unicode):
		raise ValueError('user_id must be unicode.')
	
	port_item = Portfolio(user_id=user_id, cash_balance=0.0)
	port_item.save()
	return port_item


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

def user_signup(email, username, password, exchange):
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
		create_portfolio(user.objectId)
		update_ledger(exchange.objectId, user.objectId, 100.0)
	except Exception as err:
		# delete created user if error in update_ledger
		user.delete()
		raise Exception(err)

	return user

def create_company(name, ticker):
	"""
	create parse company object
	"""
	if not isinstance(name, str):
		raise ValueError('name must be string.')
	if not isinstance(ticker, str):
		raise ValueError('ticker must be string.')
	
	#check for duplicate companies
	companies = Company.Query.all().filter(ticker=ticker)
	count = sum([1 for i in companies])
	if count:
		raise Exception('Company with this ticker already in db.')

	companies = Company.Query.all().filter(name=name)
	count = sum([1 for i in companies])
	if count:
		raise Exception('Company with this name already in db.')
	
	company = Company(name=name, ticker=ticker)
	company.save()
	return company

def get_company_by_ticker(ticker):
	"""
	finds company in parse db matching ticker
	"""
	if not isinstance(ticker, str):
		raise ValueError('ticker must be string.')
	company = Company.Query.get(ticker=ticker)
	return company

def create_ipo_object(ticker, price, auth):
	"""
	creates an parse db object to represent the shares made available in a public offering for a company
	
	ticker - string representing company ticker
	px - float representing price per shares
	auth - int representing number of shares available for purchase
	
	sold - int representing estimated number of shares sold from ipo
	"""
	if not isinstance(ticker, str):
		raise ValueError('ticker must be string.')
	if not isinstance(price, float):
		raise ValueError('price must be float.')
	if not isinstance(auth, int):
		raise ValueError('auth must be int.')
	if price <= 0:
		raise ValueError('price must be positive.')
	if auth <= 0:
		raise ValueError('auth must be positive.')
	
	company = get_company_by_ticker(ticker)

	#check for duplicate companies
	ipo_objects = IPO.Query.all().filter(company_id=company.objectId)
	count = sum([1 for i in ipo_objects])
	if count:
		raise Exception('IPO object for this company in db.')

	ipo_object = IPO(company_id=company.objectId, ticker=ticker, price=price, auth=auth)
	ipo_object.save()
	return ipo_object


def buy_ipo_shares(user_id, ticker, quantity):
	
	if not isinstance(user_id, unicode):
		raise ValueError('user_id must be unicode.')
	if not isinstance(ticker, str):
		raise ValueError('ticker must be string.')
	if not isinstance(quantity, int):
		raise ValueError('quantity must be int.')

	try:
		ipo_object = IPO.Query.get(ticker=ticker)
	except Exception as err:
		raise Exception('No IPO object available for that ticker - %s' % (err))
	
	pass 


def update_ledger(from_user_id, to_user_id, amount, ticker=None, share_price=None, share_quantity=None, fees=None):
	"""
	a recording of transferred assets

	from_user_id - string - parse object id of user tansfering assets
	to_user_id - string - parse object id of user accepting transferred assets
	amount - float - cash value of transfer, not including fees
	ticker - string 
	share_price - float
	share_quantity - int
	fees - float
	"""
	"""
	if not isinstance(user_id, unicode):
		raise ValueError('user_id must be unicode.')
	if not isinstance(amount, float):
		raise ValueError('amount must be float.')
	"""
	ledger_item = Ledger(from_user_id=from_user_id, to_user_id=to_user_id, amount=amount,)
	for i in (ticker, share_price, share_quantity, fees):
		if i:
			setattr(ledger_item, str(i), i)
	ledger_item.save()
	return ledger_item


if __name__ == "__main__":
	
	from settings import PARSE_CONFIG
	from parse_rest.connection import register
	register(PARSE_CONFIG['app_id'], PARSE_CONFIG['api_key'])
	