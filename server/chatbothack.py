from flask import *
from RegistrationForm import RegistrationForm
from flask import Flask
from flask import render_template
from twilio_helper import send_text
from crystal_knows import *
lst = {"Leo": ["Leo", "Ojars%20Josts"]}

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/index")
def index():
    return render_template('index.html', title="index")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # form.username.data, form.email.data,
        # form.password.data
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/send_text_test')
def text_test():
    exNumber = "+447873124771"
    text = "Hi, there!"
    send_text(exNumber, text)
    return "Done"


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
