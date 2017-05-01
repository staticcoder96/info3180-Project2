from app import db
class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))
    username = db.Column(db.String(80))

    def __init__(self,name,password,email,fname,lname):
        self.last_name=lname
        self.first_name=fname
        self.username = name
        self.password = password
        self.email = email
    def __repr__(self):
        return '<User %r>' % self.username
        
class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    title = db.Column(db.String(80))
    desc = db.Column(db.String(120))
    def __init__(self, userid, title, desc):
        self.userid = userid
        self.title =  title
        self.desc = desc
    def __repr__(self):
        return '<Wishlist %r>' % self.title
        
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    item_url = db.Column(db.String(120))
    title = db.Column(db.String(80))
    desc = db.Column(db.String(80))
    def __init__(self, userid, title, desc, item_url):
        self.userid = userid
        self.title =  title
        self.desc = desc
        self.item_url = item_url
    def __repr__(self):
        return '<Item %r>' % self.title