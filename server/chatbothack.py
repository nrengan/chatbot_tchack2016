from flask import Flask
from flask import render_template
import twilio_helper

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/index")
def index():
    return render_template('index.html', title="index")

@app.route('/send_text_test')
def text_test():
	send_text()
	return "Done"

if __name__ == '__main__':
    app.run()
