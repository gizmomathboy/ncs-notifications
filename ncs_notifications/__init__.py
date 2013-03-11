from flask import Flask, request
from postmonkey import PostMonkey
from mandrill import Mandrill
from pprint import pformat
import datetime


print __name__
app = Flask(__name__)

# Configuration
app.config.from_object('settings.config.Config')


@app.route('/')
def home():
    return('hello there')


@app.route('/sendabunch', methods=['POST'])
def sendabunch():
    md = Mandrill(app.config['MD_API_KEY'])

    email = request.form['email']
    count = request.form.get('count', 1)
    msg_text = "Hello, test user!\n\nThis was sent on %s\n" % datetime.datetime.now()

    for n in range(0, count):
        message = {
            "text": msg_text,
            "subject": "Sendabunch Test Emails",
            "from_email": app.config['DEFAULT_FROM_EMAIL'],
            "from_name": app.config['DEFAULT_FROM_NAME'],
            "to": [{
                "email": email
            }]
        }

        app.logger.debug("sending to %s" % (email))

        resp = md.messages.send(message)

        app.logger.debug(pformat(resp))

    return('done sent')


@app.route('/emailme')
def emailme():

    """
    sends emails to a configured MailChimp list
    """

    pm = PostMonkey(app.config['PM_API_KEY'])
    md = Mandrill(app.config['MD_API_KEY'])

    members = pm.listMembers(id=app.config['PM_LIST_ID'], limit=1000)
    emails = []

    for mem in members['data']:
        emails.append(mem['email'])

    msg_html = "<h1> hello, testing user! </h1>"

    for email in emails:
        message = {
            "html": msg_html,
            "subject": "List sends test",
            "from_email": app.config['DEFAULT_FROM_EMAIL'],
            "from_name": app.config['DEFAULT_FROM_NAME'],
            "to": [{
                "email": email
            }]
        }

        app.logger.debug("sending to %s" % (email))

        resp = md.messages.send(message)

        app.logger.debug(pformat(resp))

    return(', '.join(emails))
