from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, StringField,PasswordField,SubmitField,FileField,SelectField
from wtforms.validators import DataRequired,Required

class LoginForm(Form):
    email = StringField('Email', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Login')
class SignUpForm(Form):
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    email = StringField('Email', validators=[Required()])
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    submit = SubmitField('Sign Up')
class WishForm(Form):
    title = StringField('Title', validators=[Required()])
    description = TextAreaField('Description')
    url = StringField('Search For Image',validators=[Required()])
    submit = SubmitField('Add Wish')
class ShareForm(Form):
    email = StringField('Email', validators=[Required()])
    submit = SubmitField('Share Wishlist')

    