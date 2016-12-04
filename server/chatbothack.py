from crystal_knows import *
from flask import *
from twilio_helper import send_text
from saltedge_helper import *
from database import *
import unicodedata

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

@app.route("/login")
@app.route("/login.html")
def login_page():
	id = request.args.get('id')
	return render_template('/login.html', id = id)

@app.route('/newCustomer/<string:id>')
def create_new_customer(id="exampleID"):
	record = loadData()
	headers = { 'Accept': 'application/json', 'Client-id' : 'UDbWPMg0eJ8-_RlC5k7Thw', 'App-secret' : 'jvcjbJPm9-TUXBRLf3LK6nDgHsiz9xD6yrjJgPYA5Bg', 'Content-Type' : 'application/json' }
	r = get_new_customer(headers, unicodedata.normalize('NFKD', id).encode('ascii','ignore'))
	headers['Customer-secret'] = unicodedata.normalize('NFKD', r['data']['secret']).encode('ascii','ignore')
	r = get_new_login(headers)
	headers['Login-secret'] = unicodedata.normalize('NFKD', r['data']['secret']).encode('ascii','ignore')
	record['headers'][id] = headers
	saveData()
	return json.dumps(headers)
	# r = get_new_account(headers)
	
	# # r = requests.get('https://www.saltedge.com/api/v3/accounts', headers = headers).content
	# print(json.loads(r))
	# return json.dumps(headers)

@app.route('/newAccount/<string:id>')
def create_new_account(id="exampleID"):
	record = loadData()
	r = get_new_account(record['headers'][id])
	return r

@app.route('/newTransactions/<string:id>')
def create_new_transactions(id="exampleID"):
	record = loadData()
	r = get_transactions(record['headers'][id])
	return r

@app.route('/loginWithUsername', methods=['POST'])
def login_with_username():
    username = request.form['username']
    password = request.form['password']
    fid = request.form['id']
    record['username'][fid] = {"username": username, 'password' : password}
    return "Done"


@app.route('/send_text_test')
def text_test():
    exNumber = "+447873124771"
    text = "Hi, there!"
    send_text(exNumber, text)
    return "Done"

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('Webapp', path)

# region "Bot commands"
users = {}
potential_users = {}


@app.route('/linkedin')
def linked_in_check():
    uid = request.args.get('uid')
    if uid not in users:
        fname = request.args.get('fname')
        pers_details = person_details(person_query(fname if fname not in lst else lst[fname][0], request.args.get('lname') if fname not in lst else lst[fname][1]), 0)

        response = {"messages": [
            {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [{
                            "title": "LinkedIn Connect",
                            "image_url": pers_details['person']['photo_url'],

                        }],
                    },

                }

            },
            {
                "text": "Is this your linkedin profile?",
                "quick_replies": [
                    {"title": "Yes", "block_names": ["linkedin_link"]},
                    {"title": "No", "block_names": ["linkedin_fail"]}
                ]

            }
        ]}
        potential_users[uid] = {'name': request.args.get('fname') + request.args.get('lname'), 'id': uid,
                                'linkedin_details': pers_details['person']}
        return jsonify(**response)
        #               'personality': personality_type(pers_details)}
    else:
        return "You appear to already be connected to LinkedIn"


@app.route('/linkedin_confirm')
def linked_in_confirm():
    uid = request.args.get('uid')
    users[uid] = potential_users[uid]
    response = {"messages": [
        {
            "text": "Awesome, your LinkedIn account has been added, and we'll now tailor responses based on your personality.",
            "quick_replies": [
                {"title": "Continue", "block_names": ["C.5. Psychological profile results"]},
            ]
        }
    ]}

    return jsonify(**response)

# endregion


if __name__ == '__main__':
    app.run()
