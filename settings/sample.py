# a sample config file. use env var to pass this run.py
#
# > export NCS_NOTIFICATION_SETTINGS=/var/www/ncs-notifications/settings/sample.py; python run.py

DEBUG = True

PM_API_KEY = 'MAILCHIMP_KEY'
PM_LIST_ID = u'MAILCHIMP_LIST_ID'
MD_API_KEY = 'MANDRILL_KEY'

DEFAULT_FROM_EMAIL = 'postmaster@from.domain'
DEFAULT_FROM_NAME = 'Postmaster'
