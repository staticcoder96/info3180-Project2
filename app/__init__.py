from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import smtplib


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://project01:wishlist@localhost/project01'
app.config['SECRET_KEY']='shh..itsasecret'
app.config['UPLOAD_FOLDER'] = "./app/static/UPLOADS"
db = SQLAlchemy(app)
db.create_all()
db.session.commit()
from app import views,models
