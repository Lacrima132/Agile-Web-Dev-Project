from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    uid = db.Column(db.Integer, primary_key=True) #turn back to ID if it doesnt work and make sure to change foreign key parameters below back to 'id' as well if required
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    name = db.Column(db.String(150))
    avatar = db.Column(db.String(150), default = "pfp.png")
    bio = db.Column(db.String(150), default="Nothing here yet!")
    rank = db.Column(db.String(150), default = "D")
    isHunter = db.Column(db.Boolean, default=False)
    promote = db.Column(db.Integer, default=0)

    def get_id(self):
        return str(self.uid)  # Ensure it returns a string, as expected by Flask-Login

class Post(db.Model): #discussion posts, flag = "discussion"
    pid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    user = db.relationship('User', backref='post')
    title = db.Column(db.String(100))
    img = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(1000))
    flag = db.Column(db.String(100)) #Bounty, Listing, Discussion
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    likes = db.Column(db.Integer, default = 0)
    dislikes = db.Column(db.Integer, default = 0)
    price = db.Column(db.Integer, default = 0)
    status = db.Column(db.String(100))
    com_num = db.Column(db.Integer, default = 0)
    claimed = db.Column(db.String(100), default=False) #if the logged in user has claimed this bounty or not
    
    
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
    uid = db.Column(db.Integer, db.ForeignKey('user.uid')) #who is selling the item
    user = db.relationship('User', backref='sell')
    price = db.Column(db.Integer)
    title = db.Column(db.String(100))
    img = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(1000))
    sold = db.Column(db.String(100), default="Unsold") #changes to user logged in who bought it
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    flag = db.Column(db.String(100))
    com_num = db.Column(db.Integer, default = 0)
    
class Promote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    promoted_by=db.Column(db.Integer, db.ForeignKey('user.uid'))
    promoting_this_guy=db.Column(db.Integer)
    promoted = db.Column(db.Boolean, default=False)

# class Bounty(db.Model):
#     id = db.Column
