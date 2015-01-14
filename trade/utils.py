from parse_rest.datatypes import Object
from parse_rest.user import User as ParseUser

import datetime
from django.utils.timezone import utc
from random import choice
import pyrise
import string

from settings import HIGHRISE_CONFIG, DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, LIVE

from django.core.mail import send_mail, get_connection, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from inlinestyler.utils import inline_css

import django_rq
redis_conn = django_rq.get_connection()


def offer(user, dir, quant, px=None):
	"""
	user - parse user id
	dir - str 'buy' or 'sell'
	quant - int num shares
	px - None if market, float if limit
	"""
	pass



if __name__ == "__main__":
	
	print "hi"