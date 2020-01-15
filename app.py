from flask import Flask, session,render_template, request, redirect, g, send_from_directory
import time
from sqlalchemy.dialects.postgresql import UUID
import json
from flask_login import LoginManager, UserMixin,logout_user, login_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, static_url_path='')

#create_engine('sqlite:///C:\\path\\to\\foo.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
app.config['SECRET_KEY'] = 'secret'

#engine = create_engine('sqlite:///E:\\GreivancePortal\\portal.db')

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

@app.route('/', methods = ["GET"])
def index():
    if current_user.is_authenticated:
         return render_template("main.html")
    else:
         return render_template("index.html")

@app.route('/login', methods = ['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email = email).first()
    if check_password_hash(user.password, password):
        login_user(user)
    
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()    
    return redirect('/')

@app.route('/register', methods = ['POST'])
def register():
    print(request.form)
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
   
    return redirect('/')


@app.route('/submitgrievance', methods = ['POST'])
@login_required
def submit():
    form = request.get_json()
    new_g = {'user':form['user'],
             'type': form['type'], 
             'department':form['department'], 
             'text':form['text'], 
             'mood':None, 
             }

    greivance.append(new_g)
    return "Your Grievance has been submitted"


@app.route('/listgrievance', methods = ['GET'])
def list():
   return json.dumps(grievance)


if __name__ == '__main__':
    app.debug = True
    app.run(port = 3000)
    
