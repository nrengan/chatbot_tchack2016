# Download the twilio-python library from http://twilio.com/docs/libraries
# import twilio
# from twilio import *
# from twilio.rest import *
from twilio.rest import TwilioRestClient

def send_text(send_to_number, text) :
	# Find these values at https://twilio.com/user/account
	account_sid = "AC78291078bf12a4f632415fa544390585"
	auth_token = "4eb792cf644d34acb90db9805b99c60c"
	client = TwilioRestClient(account_sid, auth_token)
	
	message = client.messages.create(to=send_to_number, from_="+441172001580", body=text)
	print(message)
	
