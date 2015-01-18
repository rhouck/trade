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
	if not isinstance(exchange, ParseUser):
		raise ValueError('exchange must be parse user object.')

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

def create_ipo_object(ticker, price, auth, exchange):
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
	if not isinstance(exchange, ParseUser):
		raise ValueError('exchange must be parse user object.')


	company = get_company_by_ticker(ticker)

	#check for duplicate companies
	ipo_objects = IPO.Query.all().filter(company_id=company.objectId)
	count = sum([1 for i in ipo_objects])
	if count:
		raise Exception('IPO object for this company in db.')

	ipo_object = IPO(company_id=company.objectId, ticker=ticker, price=price, auth=auth)
	ipo_object.save()

	# update exchnage portfolio
	value_updates = {ticker: auth}
	update_portfolio_object(exchange.objectId, value_updates)
	
	return ipo_object

def update_portfolio_object(user_id, value_updates):
	"""
	creates a new portfolio object to reflect changes to cash balance or share ownership
	it first creats a portfolio object matching user generated values in most recently created portfolio object

	user_id - parse user object id
	value_updates - a dictionary containing the items to update as keys and the values by which to agument current values in as values
	"""
	if not isinstance(user_id, unicode):
		raise ValueError('user_id must be unicode.')
	if not isinstance(value_updates, dict):
		raise ValueError('value_updates must be dict with portfolio item as key and desired change in value as value.')

	current_portfolio = Portfolio.Query.filter(user_id=user_id).order_by("-createdAt").limit(1)[0]
	new_portfolio = duplicate_parse_object(Portfolio, current_portfolio)

	current_portfolio_items = new_portfolio.__dict__.keys()
	for k, v in value_updates.iteritems():
		if k in current_portfolio_items:
			setattr(new_portfolio, k, getattr(new_portfolio, k) + v)
		else:
			setattr(new_portfolio, k, v)
	new_portfolio.save()
	return new_portfolio

def duplicate_parse_object(object_type, current_state):
	"""
	use to create new parse object with identical user generated values as existing object
	this can be used as part of the process of creating updated states of portfolio objects
	
	object_type - the parse object class name you want to create a new instance of
	current_state - an instnace of object_type that contains user generated values you want to duplicate
	"""
	if not isinstance(object_type, object) or not isinstance(current_state, object):
		raise ValueError('object_type and current_state must both be objects.')
	
	new = object_type()
	ignore = ('_created_at', '_updated_at', 'objectId')
	for k, v in current_state.__dict__.iteritems():
		if k not in ignore:
			setattr(new, str(k), v)
	return new

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
	