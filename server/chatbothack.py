from flask import *

from flask import Flask, request, send_from_directory
from flask import render_template
from twilio_helper import send_text
from saltedge_helper import *
from database import *
import unicodedata
import requests

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
@app.route('/')
@app.route("/index")
@app.route("/index.html")
def index():
	data = []
	return render_template('/index.html', data = data)

@app.route("/register")
@app.route("/register.html")
def register_page():
	data = []
	return render_template('/register.html', data = data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # form.username.data, form.email.data,
        # form.password.data
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/newCustomer/<string:id>')
def create_new_customer(id="exampleID"):
	record = loadData()
	headers = { 'Accept': 'application/json', 'Client-id' : 'UDbWPMg0eJ8-_RlC5k7Thw', 'App-secret' : 'jvcjbJPm9-TUXBRLf3LK6nDgHsiz9xD6yrjJgPYA5Bg', 'Content-Type' : 'application/json' }
	r = get_new_customer(headers, unicodedata.normalize('NFKD', id).encode('ascii','ignore'))
	headers['Customer-secret'] = unicodedata.normalize('NFKD', r['data']['secret']).encode('ascii','ignore')
	r = get_new_login(headers)
	headers['Login-secret'] = unicodedata.normalize('NFKD', r['data']['secret']).encode('ascii','ignore')
	record[id] = headers
	saveData()
	return json.dumps(headers)
	# r = get_new_account(headers)
	
	# # r = requests.get('https://www.saltedge.com/api/v3/accounts', headers = headers).content
	# print(json.loads(r))
	# return json.dumps(headers)

@app.route('/newAccount/<string:id>')
def create_new_account(id="exampleID"):
	print(id)
	record = loadData()
	print(record)
	print(record[id])
	r = get_new_account(record[id])
	return r

@app.route('/newTransactions/<string:id>')
def create_new_transactions(id="exampleID"):
	record = loadData()
	r = get_transactions(record[id])
	return r

@app.route('/send_text_test')
def text_test():
    exNumber = "+447873124771"
    text = "Hi, there!"
    send_text(exNumber, text)
    return "Done"

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('Webapp', path)

if __name__ == '__main__':
    app.run()
