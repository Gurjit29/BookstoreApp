
from app import login
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    key=db.Column(db.String(130))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
   
    def __repr__(self):
        return '<User {} {}>'.format(self.username,self.id)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(350))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id=db.Column(db.Integer, db.ForeignKey('book.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Book(db.Model):
   id=db.Column(db.Integer, primary_key=True)
   writer=db.Column(db.String(100))
   title=db.Column(db.String(100))
   description=db.Column(db.String(350))
   url=db.Column(db.String(150))
   cost=db.Column(db.Float)
   quantity=db.Column(db.Integer)
   posts=db.relationship('Post',backref='review', lazy='dynamic')

   def __repr__(self):
       return '<Book {} >'.format(self.description)
   
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
