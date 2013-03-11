import sys
import os
import logging

cwd = os.getcwd()

# append current dir to module path
sys.path.append(cwd)

# set path to the python interpreter in the virtualenv
INTERP = os.path.join(cwd, 'bin', 'python')

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# add the /site directory to the sysoath so we can import the app
sys.path.append(os.path.join(cwd, 'site'))


## LOGGING

# create a logfile in the current directory
logfilename = os.path.join(cwd, 'passenger_wsgi.log')
# configure the logging
logging.basicConfig(filename=logfilename, level=logging.DEBUG)
logging.info("Running %s", sys.executable)


def application(environ, start_response):
    from ncs_notifications import app

    logging.info("Application called:")
    logging.info("environ: %s", str(environ))
    results = []
    try:
        results = app(environ, start_response)
        logging.info("App executed successfully")
    except Exception, inst:
        logging.exception("Error: %s", str(type(inst)))
    logging.info("Application call done")
    return results
