from flask import Flask

print __name__
app = Flask(__name__)


@app.route('/poop')
def home():
    return('poop')
