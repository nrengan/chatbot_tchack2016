# Download the twilio-python library from http://twilio.com/docs/libraries
# import twilio
# from twilio import *
# from twilio.rest import *
from twilio.rest import TwilioRestClient

def send_text() :
	print('AAAAA')
	# Find these values at https://twilio.com/user/account
	account_sid = "AC78291078bf12a4f632415fa544390585"
	auth_token = "4eb792cf644d34acb90db9805b99c60c"
	print('check 1')
	client = TwilioRestClient(account_sid, auth_token)
	print('check 2')	
	message = client.messages.create(to="+447873124771", from_="+447448450373", body="Hello there!")
	print('check 3')
	
