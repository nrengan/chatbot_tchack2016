from flask import *

from RegistrationForm import RegistrationForm
from flask import Flask
from flask import render_template
from twilio_helper import send_text

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


if __name__ == '__main__':
    app.run()
