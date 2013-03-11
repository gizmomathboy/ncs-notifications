from flask import Flask, request, render_template, flash, redirect, url_for
from postmonkey import PostMonkey
from mandrill import Mandrill
from pprint import pformat
import datetime
from .basic_auth import requires_auth

app = Flask(__name__)

# Configuration
app.config.from_object('settings.config.Config')


# handlers
@app.route('/')
@requires_auth
def home():
    return render_template('post_form.html',
                           page_title="E-Mail Post Form",
                           default_from_name=app.config["DEFAULT_FROM_NAME"],
                           default_from_email=app.config["DEFAULT_FROM_EMAIL"])


@app.route('/review', methods=['POST'])
@requires_auth
def review():

    app.logger.debug(request.form)

    # get form data (WE SHOULD VALIDATE)
    message = request.form.get('message')
    subject = request.form.get('subject')
    from_email = request.form.get('from_email')
    from_name = request.form.get('from_name')

    return render_template('review_form.html',
                           page_title="Review E-mail",
                           from_name=from_name,
                           from_email=from_email,
                           message=message,
                           subject=subject)


@app.route('/send', methods=['POST'])
def send():
    """
    sends emails to a configured MailChimp list
    """

    # get form data (WE SHOULD VALIDATE)
    msg_text = request.form.get('message_confirmed')
    subject = request.form.get('subject_confirmed')
    from_email = request.form.get('from_email_confirmed')
    from_name = request.form.get('from_name_confirmed')

    pm = PostMonkey(app.config['PM_API_KEY'])
    md = Mandrill(app.config['MD_API_KEY'])

    members = pm.listMembers(id=app.config['PM_LIST_ID'], limit=1000)
    emails = []

    for mem in members['data']:
        emails.append(mem['email'])

    now = datetime.datetime.now()
    msg_text = "%s\n\n--------\n\nE-mail generated at %s" % (msg_text, now)

    for email in emails:
        message = {
            "text": msg_text,
            "subject": subject,
            "from_email": from_email,
            "from_name": from_name,
            "to": [{
                "email": email
            }]
        }

        app.logger.debug("sending to %s" % (email))

        resp = md.messages.send(message)

        app.logger.debug(pformat(resp))

    flash("%s e-mails sent!" % len(emails))

    return redirect(url_for('home'))


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

    flash("%s e-mails sent!" % count)

    return redirect(url_for('home'))
