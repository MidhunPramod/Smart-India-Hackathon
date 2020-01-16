from flask import Flask, session,render_template, request, redirect, g, send_from_directory, jsonify
import time
from sqlalchemy.dialects.postgresql import UUID
import json
from flask_login import LoginManager, UserMixin,logout_user, login_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from uuid import uuid4

app = Flask(__name__, static_url_path='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads/files') #'/uploads/files'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

def generate_uuid():
    return str(uuid4())

class User(UserMixin, db.Model):
    
    id = db.Column(db.String(256), unique=True, nullable=False, default = generate_uuid, primary_key = True)
    name = db.Column(db.String(32))
    email = db.Column(db.String(32), unique = True)
    password = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, server_default = db.func.now(), server_onupdate = db.func.now())

    def to_json(self):
        return { 'id':self.id,'name':self.name,
            'email':self.email,
            'password':self.password,
            'created_at':self.created_at,
            'updated_at':self.updated_at}

class Grievance(db.Model):
    id = db.Column(db.String(256), unique = True, primary_key = True, default = generate_uuid)
    
    u_id = db.Column(db.String(200))
    g_type = db.Column(db.String(200),nullable=False)
    institute = db.Column(db.String(200),nullable=False)
    content = db.Column(db.String(2000),nullable=False)
    feedback = db.Column(db.String(200))
    status = db.Column(db.String(200))
    mood = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, server_default = db.func.now(), server_onupdate = db.func.now())

    def to_json(self):
        return { 'id':self.id,'u_id':self.u_id,
            'g_type':self.g_type,
            'institute':self.institute,
            'content':self.content,
            'feedback':self.feedback,
            'status':self.status,
            'mood':self.mood,
            'created_at':self.created_at,
            'updated_at':self.updated_at}

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
    if current_user.is_authenticated:
        logout_user()
    
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']
    name = request.form['name']

    user = User()

    user.email = email
    user.password = generate_password_hash(password)
    user.name = name

    db.session.add(user)
    db.session.commit()

    return redirect('/')


@app.route('/submitgrievance', methods = ['POST'])
@login_required
def submit():
    form = request.form

    new_g = Grievance()
    
    new_g.g_type = form['type']
    new_g.u_id = current_user.id
    new_g.institute = form['institute']
    new_g.content = form['content']

    db.session.add(new_g)
    db.session.commit()

    return redirect('/')

@app.route('/status', methods = ['GET'])
@login_required
def status():
    grievances = Grievance.query.filter_by(u_id = current_user.id).all()
    f = []

    for i in grievances:
        f.append(i.to_json())
    
    return jsonify(f)

@app.route('/uploadtest', methods = ['POST'])
def upload():
    if request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #return redirect(url_for('uploaded_file', filename=filename))
        return 'okay'

if __name__ == '__main__':
    app.debug = True
    app.run(port = 3000)
    
