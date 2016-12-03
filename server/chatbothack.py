from flask import *

from flask import Flask, request, send_from_directory
from flask import render_template
from twilio_helper import send_text
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
