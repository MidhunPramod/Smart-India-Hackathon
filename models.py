from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from uuid import uuid4
from flask_login import UserMixin

app = Flask(__name__, static_url_path='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

class Institutes(db.Model):
	name = db.Column(db.String(32), unique = True, primary_key = True)

class GrievanceTypes(db.Model):
	type = db.Column(db.String(32), unique = True, primary_key = True)


def generate_uuid():
    return str(uuid4())

class User(UserMixin, db.Model):
    
    id = db.Column(db.String(256), unique=True, nullable=False, default = generate_uuid, primary_key = True)
    name = db.Column(db.String(32))
    email = db.Column(db.String(32), unique = True)
    password = db.Column(db.String(32))
    institute = db.Column(db.String(32))
    access = db.Column(db.Integer, default = 0)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, server_default = db.func.now(), server_onupdate = db.func.now())

    def to_json(self):
        return { 'id':self.id,'name':self.name,
            'email':self.email,
            'password':self.password,
            'created_at':self.created_at,
			'access' : self.access,
            'updated_at':self.updated_at}

class Grievance(db.Model):
    id = db.Column(db.String(256), unique = True, primary_key = True, default = generate_uuid)
    
    u_id = db.Column(db.String(256))
    g_type = db.Column(db.String(256),nullable=False)
    institute = db.Column(db.String(256),nullable=False)
    subject = db.Column(db.String(256), nullable = False)
    content = db.Column(db.String(2048),nullable=False)
    feedback = db.Column(db.String(256))
    status = db.Column(db.String(256))
    mood = db.Column(db.String(256))
    #tags = db.Column(db.String(256))

    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, server_default = db.func.now(), server_onupdate = db.func.now())

    def to_json(self):
        return { 'id':self.id,'u_id':self.u_id,
            'g_type':self.g_type,
            'institute':self.institute,
            'content':self.content,
            'feedback':self.feedback,
            'status':self.status,
            'subject':self.subject,
            'mood':self.mood,
            'created_at_words':self.created_at.strftime('%H:%M, %d %B %Y'),
            'updated_at_words':self.updated_at.strftime('%H:%M, %d %B %Y'),
            'created_at':self.created_at,
            'updated_at':self.updated_at}