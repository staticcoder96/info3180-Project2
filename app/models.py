from app import db
class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))
    username = db.Column(db.String(80))

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email
    def __repr__(self):
        return '<User %r>' % self.firstname
class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    title = db.Column(db.String(80))
    desc = db.Column(db.String(120))
    created_on = db.Column(db.String(80))
    isprivate = db.Column(db.Integer)
    def __init__(self, userid, title, desc, isprivate, created_on):
        self.userid = userid
        self.title =  title
        self.desc = desc
        self.isprivate = isprivate
        self.created_on = created_on
    def __repr__(self):
        return '<Wishlist %r>' % self.title
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    wishlistid = db.Column(db.Integer)
    item_url = db.Column(db.String(120))
    title = db.Column(db.String(80))
    desc = db.Column(db.String(80))
    image_url = db.Column(db.String(120))
    added_on = db.Column(db.String(80))
    def __init__(self, userid, wishlistid, title, desc, image_url, item_url, added_on):
        self.userid = userid
        self.wishlistid = wishlistid
        self.title =  title
        self.desc = desc
        self.image_url = image_url
        self.item_url = item_url
        self.added_on = added_on
    def __repr__(self):
        return '<Item %r>' % self.title