from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import smtplib


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://project01:wishlist@localhost/project01'
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://vjmyqsccqutxaw:6a151746ead95f3a8f14136851adccfc248f4355e722c2a8257cb8784840a062@ec2-54-235-72-121.compute-1.amazonaws.com:5432/d1u4ulsb830vdc'
app.config['SECRET_KEY']='shh..itsasecret'
app.config['UPLOAD_FOLDER'] = "./app/static/UPLOADS"
db = SQLAlchemy(app)
db.create_all()
db.session.commit()
from app import views,models
