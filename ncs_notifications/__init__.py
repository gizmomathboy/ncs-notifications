from flask import Flask, request, render_template, Response
from postmonkey import PostMonkey
from mandrill import Mandrill
from pprint import pformat
from functools import wraps
import datetime


app = Flask(__name__)

# Configuration
app.config.from_object('settings.config.Config')


# auth functions
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    auth_username = app.config['AUTH_USERNAME']
    auth_password = app.config['AUTH_PASSWORD']
    return username == auth_username and password == auth_password


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# handlers
@app.route('/')
@requires_auth
def home():
    return render_template('index.html')


@app.route('/sendabunch', methods=['POST'])
@requires_auth
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
@requires_auth
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
