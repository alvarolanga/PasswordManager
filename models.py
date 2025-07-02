from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy() #Starts the SQL Alchemy for database

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True) #unique User ID
    username = db.Column(db.String(150), unique=True, nullable=False) #Username must be distinctive
    password_hash = db.Column(db.String(256), nullable=False) #hashed password will be stored safely

    credentials = db.relationship('Credential', backref='owner', lazy=True)  #1-TO-Many

    def set_password(self, password):
        self.password_hash = generate_password_hash(password) #hash and store password

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) #check password


class Credential(db.Model):
    __tablename__ = 'credential'

    id = db.Column(db.Integer, primary_key=True) #unique credential id
    service = db.Column(db.String(150), nullable=False) #name of the service
    username = db.Column(db.String(150), nullable=False) #username of the service
    password_encrypted = db.Column(db.LargeBinary, nullable=False) #encrypted password stored securely
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
