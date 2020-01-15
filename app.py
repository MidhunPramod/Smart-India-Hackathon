from flask import Flask, session, render_template, request, redirect, g
import time
from sqlalchemy.dialects.postgresql import UUID
import pickle
import os
import json
from flask_login import LoginManager, UserMixin,logout_user, login_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

#create_engine('sqlite:///C:\\path\\to\\foo.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:\\GrievancePortal\\portal.db'
app.config['SECRET_KEY'] = 'secret'

#engine = create_engine('sqlite:///E:\\GreivancePortal\\portal.db')

grievance = []

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, unique = True, primary_key = True)
    #id = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    name = db.Column(db.String(32))
    email = db.Column(db.String(32), unique = True)
    password = db.Column(db.String(32))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods = ['POST'])
def index():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email = email).first()
    if check_password_hash(user.password, password):
        login_user(user)
        return "You are now Logged In " + current_user.name
    else:
        return "Wrong Info, Dude"

@app.route('/logout')
@login_required
def logout():
    logout_user()    

@app.route('/register', methods = ['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password']
    name = request.form['name']

    user = User()

    user.email = email
    user.password = generate_password_hash(password)
    user.name = name

    id = 1

    db.session.add(user)
    db.session.commit()
   
    return "Submitted"


@app.route('/submitgrievance', methods = ['POST'])
@login_required
def submit():
    form = request.get_json()
    new_g = {'user':form['user'], 'type': form['type'], 'department':form['department'], 'text':form['text'], 'mood':None, 'time':time.asctime()}
    greivance.append(new_g)
    return "Your Grievance has been submitted"


@app.route('/listgrievance', methods = ['GET'])
def list():
   return json.dumps(grievance)


if __name__ == '__main__':
    app.debug = True
    app.run(port = 8080)
    
