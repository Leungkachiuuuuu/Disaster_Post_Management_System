from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(40)) #either donor,
    #recipient or call center operator, admin
    user_status = db.Column(db.String(10)) #has the user of user_type "recipient" 
    #been acknowledged as legitimate by the call center operator. takes 2 values
    #acive, inactive
    posts = db.relationship('DisasterPost', backref='author', lazy='dynamic')
    user_address = db.Column(db.VARCHAR(150))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class DisasterPost(db.Model): #table to store disaster requirements
    post_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    created_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    location_latitude =  db.Column(db.Float, default=0.0)
    location_longitude =  db.Column(db.Float, default=0.0)
    recipient_address = db.Column(db.VARCHAR(150))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class ReliefItems(db.Model):
	item_id = db.Column(db.Integer, primary_key=True)
	item_name = db.Column(db.String(64), index=True, unique=True)


class ItemQuantity(db.Model):
	item_quantity_id = db.Column(db.Integer, primary_key=True)
	quantity_needed = db.Column(db.Integer, default=0)
	relief_item = db.Column(db.Integer, db.ForeignKey('relief_items.item_id'))
	disaster = db.Column(db.Integer, db.ForeignKey('disaster_post.post_id'))
