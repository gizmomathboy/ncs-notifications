from ncs_notifications import app

app.config.from_object('settings.default')
app.config.from_envvar('NCS_NOTIFICATION_SETTINGS')

app.run()
