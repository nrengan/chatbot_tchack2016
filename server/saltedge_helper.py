
import json
import requests

def get_new_customer(headers, id):
	text = {"data" : {"identifier" : id}}
	return json.loads(requests.post('https://www.saltedge.com/api/v3/customers/', headers = headers, data = json.dumps(text)).content)

def get_new_login(headers):
	text = { "data": { "country_code": "XF", "provider_code": "fakebank_simple_xf", "fetch_type": "recent", "credentials": { "login": "username", "password": "secret" }}}
	return json.loads(requests.post('https://www.saltedge.com/api/v3/login', headers = headers, data = json.dumps(text)).content)

def get_new_account(headers):
	return requests.get('https://www.saltedge.com/api/v3/accounts', headers = headers).content

def get_transactions(headers):
	return requests.get('https://www.saltedge.com/api/v3/transactions', headers = headers).content
