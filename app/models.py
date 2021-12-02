from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

history = db.Table('history',
    db.Column('uid', db.Integer, db.ForeignKey('user.id')),
    db.Column('bid', db.Integer, db.ForeignKey('books.id')))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    b_history = db.relationship('Books', secondary = history, backref = 'user')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Listings(db.Model):
    __tablename__ = "listings"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    bid = db.Column(db.Integer, db.ForeignKey('books.id'))
    state = db.Column(db.String(16)) #should be values 'active' or 'nonactive'

class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.Integer, index = True, nullable = False)
    name = db.Column(db.String(64))
    author = db.Column(db.String(500))
    description = db.Column(db.String(5000))
    cover_url = db.Column(db.String(128))
