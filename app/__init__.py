from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://project01:wishlist@localhost/project01'
app.config['SECRET_KEY']='shh..itsasecret'
db = SQLAlchemy(app)
db.create_all()
from app import views,models