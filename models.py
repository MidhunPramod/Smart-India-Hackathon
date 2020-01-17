from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__, static_url_path='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

class Institutes(db.Model):
	name = db.Column(db.String(32), unique = True, primary_key = True)

class GrievanceTypes(db.Model):
	type = db.Column(db.String(32), unique = True, primary_key = True)

