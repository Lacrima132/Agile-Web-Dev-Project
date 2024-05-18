from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    uid = db.Column(db.Integer, primary_key=True) #turn back to ID if it doesnt work and make sure to change foreign key parameters below back to 'id' as well if required
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    name = db.Column(db.String(150))
    avatar = db.Column(db.String(150))
    bio = db.Column(db.String(150), default="Nothing here yet!")
    rank = db.Column(db.String(150))
    promote = db.Column(db.Integer, default=0)

    def get_id(self):
        return str(self.uid)  # Ensure it returns a string, as expected by Flask-Login

class Post(db.Model): #discussion posts, flag = "discussion"
    pid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    user = db.relationship('User', backref='post')
    title = db.Column(db.String(100))
    img_filename = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(1000))
    flag = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    likes = db.Column(db.Integer, default = 0)
    dislikes = db.Column(db.Integer, default = 0)
    
class Comments(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    user = db.relationship('User', backref='comments') 
    pid = db.Column(db.Integer, db.ForeignKey('post.pid'))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    comment = db.Column(db.String(1000))

class Likes(db.Model):
    lid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    pid = db.Column(db.Integer, db.ForeignKey('post.pid'))
    liked = db.Column(db.Boolean, default=False)
    disliked = db.Column(db.Boolean, default=False)

class Sell(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    user = db.relationship('User', backref='sell')
    price = db.Column(db.Integer)
    title = db.Column(db.String(100))
    img = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(1000))
    sold = db.Column(db.String(100), default="Unsold")
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    
class Promote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    promoted_by=db.Column(db.Integer, db.ForeignKey('user.uid'))
    promoting_this_guy=db.Column(db.Integer)
    promoted = db.Column(db.Boolean, default=False)
