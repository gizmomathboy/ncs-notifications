from flask import Flask, request, render_template, flash, redirect, url_for
from postmonkey import PostMonkey
from mandrill import Mandrill
from pprint import pformat
import pytz
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



@app.route('/edit', methods=['POST'])
@requires_auth
def edit():

    app.logger.debug(request.form)

    # get form data (WE SHOULD VALIDATE)
    msg_text = request.form.get('message')
    subject = request.form.get('subject')
    from_email = request.form.get('from_email')
    from_name = request.form.get('from_name')

    return render_template('post_form.html',
                           page_title="E-Mail Post Form",
                           default_from_name=from_name,
                           default_from_email=from_email,
                           subject=subject,
                           message=msg_text)



@app.route('/review', methods=['POST'])
@requires_auth
def review():

    app.logger.debug(request.form)

    # get form data (WE SHOULD VALIDATE)
    message = request.form.get('message')
    subject = request.form.get('subject')
    from_email = request.form.get('from_email')
    from_name = request.form.get('from_name')

    app.logger.debug(from_email)
    app.logger.debug(from_name)

    pm = PostMonkey(app.config['PM_API_KEY'])
    list_info = pm.lists(filters={'list_id':app.config['PM_LIST_ID']})
    list_name = list_info['data'][0]['name']
    list_count = list_info['data'][0]['stats']['member_count']

    return render_template('review_form.html',
                           page_title="Review E-mail",
                           from_name=from_name,
                           from_email=from_email,
                           list_name=list_name,
                           list_count=list_count,
                           message=message,
                           subject=subject)


@app.route('/send', methods=['POST'])
def send():
    """
    sends emails to a configured MailChimp list
    """

    # get form data (WE SHOULD VALIDATE)
    msg_text = request.form.get('message')
    subject = request.form.get('subject')
    from_email = request.form.get('from_email')
    from_name = request.form.get('from_name')

    pm = PostMonkey(app.config['PM_API_KEY'])
    md = Mandrill(app.config['MD_API_KEY'])

    members = pm.listMembers(id=app.config['PM_LIST_ID'], limit=1000)
    emails = []

    for mem in members['data']:
        emails.append(mem['email'])

    now_utc = datetime.datetime.now()         # get naive utc time
    local_tz = pytz.timezone('US/Eastern')    # set local timezone
    now_utc = pytz.utc.localize(now_utc)      # add timezone data to utc time
    local_time = now_utc.astimezone(local_tz) # convert to local time
    msg_text = "%s\n\n--------\n\nE-mail generated at %s" % (msg_text, local_time)
    

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

        resp = md.messages.send(message, async=True)

        app.logger.debug(pformat(resp))

    flash("%s e-mails sent!" % len(emails))

    return redirect(url_for('home'))

