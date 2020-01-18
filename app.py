import predict_sentiment
import keras.backend.tensorflow_backend as tb
print("Predict Sentiment Imported")

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


from models import Institutes, GrievanceTypes, User, Grievance

app = Flask(__name__, static_url_path='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads/files') #'/uploads/files'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/search', methods = ['POST'])
def search():
    form = request.form
    key = form['key']
    print("The search key is:", key)
    grievances = Grievance.query.filter_by(institute = current_user.institute).all()
    f = []
    
    for i in grievances:
        f.append(i.to_json())

    out = []
    print(f)
    for i in f:
        if (i['subject'] and key in i['subject']) or (i['content'] and key in i['content']) or (i['feedback'] and key in i['feedback']):
            out.append(i)
    for i, j in enumerate(out):
        print(i, j)
    return index(grievances = out)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/', methods = ["GET"])
def index(grievances = None):
    institutes = Institutes.query.all()
    institutes = [i.name for i in institutes]

    if current_user.is_authenticated:
        grievance_types = GrievanceTypes.query.all()
        grievance_types = [i.type for i in grievance_types]
        
        if current_user.access == 1:
            if grievances == None:
                grievances = adminstatus()
            return render_template("admin.html", grievance_types = grievance_types, grievances = grievances)
        else:
            return render_template("main.html", institutes = institutes, grievance_types = grievance_types, grievances = grievances)
    else:
        return render_template("index.html", institutes = institutes)

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
    
    new_g.g_type = form['g_type']
    new_g.u_id = current_user.id
    new_g.subject = form['subject']
    new_g.institute = current_user.institute
    new_g.content = form['content']
    f = new_g.id
    db.session.add(new_g)
    db.session.commit()
    model_run(f)

    return redirect('/')

# @app.route('/status', methods = ['GET'])
# @login_required

def status():
    grievances = Grievance.query.filter_by(u_id = current_user.id).all()
    f = []

    for i in grievances:
        f.append(i.to_json())
    
    return f

def adminstatus():
    grievances = Grievance.query.filter_by(institute = current_user.institute).all()
    f = []
    
    for i in grievances:
        f.append(i.to_json())
    
    return f

@app.route('/uploadtest', methods = ['POST'])
def upload():
    if request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #return redirect(url_for('uploaded_file', filename=filename))
        return 'okay'

@app.route('/submitfeedback', methods = ['POST'])
def submitfeedback():
    form = request.form

    if form:
        feedback = form['feedback']
        id = form['id']
        g = db.session.query(Grievance).get(id)
        g.feedback = feedback
        g.status = 'under_review'
        db.session.commit()
        return redirect('/')

@app.route('/closegrievance', methods = ['POST'])
def close_grievance():
    form = request.form
    id = form['id']
    g = db.session.query(Grievance).get(id)
    g.status = 'action_taken'
    db.session.commit()
    return redirect('/')

#@app.route('/modelrun', methods = ['POST'])
def run_model(id):
    tb._SYMBOLIC_SCOPE.value = True
    f = predict_sentiment.prediction(content)

    g = db.session.query(Grievance).get(id)
    f = predict_sentiment.prediction(g.content)
    g.mood = f
    db.session.commit()

if __name__ == '__main__':
    app.debug = True
    tb._SYMBOLIC_SCOPE.value = True
    app.run(port = 3000,threaded = False)
    
