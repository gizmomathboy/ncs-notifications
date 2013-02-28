from flask import Flask
from postmonkey import PostMonkey
from mandrill import Mandrill
from pprint import pprint
import datetime


print __name__
app = Flask(__name__)


@app.route('/poop')
def home():
    return('poop')


@app.route('/emailme')
def emailme():
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
            "subject": "NCS updates",
            "from_email": "webmaster@ncs.k12.in.us",
            "from_name": "NCS Webmaster",
            "to": [{
                "email": email
            }]
        }

        print "sending to %s" % (email)

        resp = md.messages.send(message)

        print pprint(resp)

    return(', '.join(emails))
