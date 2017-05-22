from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
import os


app = Flask(__name__)
modus = Modus(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/flask-blueprints'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from project.owners.views import owners_blueprint

app.register_blueprint(owners_blueprint, url_prefix='/owners')


@app.route('/')
def root():
	return "HELLO BLUEPRINTS!"