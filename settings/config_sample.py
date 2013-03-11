# a sample config file. rename to config.py


class Config(object):
    DEBUG = True

    PM_API_KEY = 'MAILCHIMP_KEY'
    PM_LIST_ID = u'MAILCHIMP_LIST_ID'
    MD_API_KEY = 'MANDRILL_KEY'

    DEFAULT_FROM_EMAIL = 'postmaster@from.domain'
    DEFAULT_FROM_NAME = 'Postmaster'
