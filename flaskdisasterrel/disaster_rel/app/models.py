from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20))#admin, advertiser, donor
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    #items = db.relationship('Item',backref='author',lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50)) 
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Items = db.relationship('Item',backref='')
    #Donate = db.relationship('donate',backref='')
    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Item(db.Model):
    __tablename__ = 'Item'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    name = db.Column(db.String(50), default='None')
    quantity = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(10), default='')
    #timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #Donate = db.relationship('Donate', backref='')

    #timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr(self):
        return '<Item {}>'.format(self.item_name)

class Donate(db.Model):
    __tablename__ = 'Donate'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    donor_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=0)
    #timestamp = db.Column(db.DateTime, default=None)


def __repr__(self):
        return '<id {}>'.format(self.id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))