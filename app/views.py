"""

Flask Documentation:     http://flask.pocoo.org/docs/

Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/

Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.

"""
from app import app,db
from app.models import Profile,Wishlist,Item
from flask import render_template, request, redirect, url_for, flash,jsonify,make_response,session
from bs4 import BeautifulSoup
from .forms import WishForm, LoginForm, SignUpForm
import validators
import requests
import urlparse
import image_getter
import os
userid=0
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


#@app.route("/thumbnails/view")
##def showImages():
#   urls= image_getter.URLs()
 #  return render_template("thumbnails.html",urls=urls)
  
@app.route("/api/users/register",methods=["GET","POST"])
def userinfo():
    """Accepts user information and saves it to the database
    """
    form = SignUpForm()
    if request.method == 'GET':
        return render_template("register.html",form=form)
    else:
        if form.validate_on_submit():
            #check that the inputs are correct
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            
        #save information to database
        user = Profile(username,password,email)
        userid=user.id
        db.session.add(user)
        db.session.commit()
        if user!=None:
            flash("User Successfully Added")
        return redirect(url_for('wishhome',userid=userid)) #brings users to their wishlist page
        


@app.route("/api/users/login", methods=["GET", "POST"])
def login():
    """Accepts login credentials as username and password
    """
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            passw = form.password.data
        
        if form.email.data and form.password.data:
            user=db.session.query(Profile).filter_by(email=email, password=passw).first()
            # get user id, load into session
            userid=user.id
            #login_user(user)
            
            flash("Logged in Successfully")
            
            return redirect(url_for('wishhome',userid=userid)) #they should be redirected to their page or wishlist
    return render_template("login.html", form=form)

    
@app.route("/api/users/{userid}/wishlist")
def wishhome():
    """Returns a users wishlist based on their user id
    """
   
    user=db.session.query(Profile).filter_by(userid).first()
    return render_template("wishlist.html",user=user)
    
@app.route("/api/users/{userid}/wishlist/{itemid}",methods=['GET','POST','DELETE'])
def wishno(userid,itemid):
    """Deletes an item from a users wishlist
    """
    if request.method == 'DELETE':
       #delete the item from the wishlist
       user = Wishlist(itemid)
       db.session.delete(user)
       db.session.commit()
       
       flash("Item Successfully Deleted")
       return redirect(url_for("wishlist.html"))
    return render_template("wishlist.html")
    
    
# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
#@login_manager.user_loader
#def load_user(id):
#    return UserProfile.get(int(id))



@app.route('/api/thumbnail/', methods=["GET","POST"])
def thumbnail():
    url="https://www.walmart.com/ip/54649026"
    #url = request.args.get('url','')
    if url == "" or not validators.url(url):
        response = jsonify({"error": "1","thumbnails":[],"message": "Unable to extract thumbnails"})
    else:
       # thumbnails = {'':get_images(url)}
        imgz=get_images(url)
        
        response=jsonify(error='Null',thumbnails=get_images(url), message="Success")
        ##return render_template("thumbnails.html",urls=response.data)
        return response
        
        
def get_images(url):
    images = []
    soup = BeautifulSoup(requests.get(url).text,"html.parser")
    imagez =soup.findAll("img",src=True)
    og_image = (soup.findAll('meta', property='og:image') or
                        soup.findAll('meta', attrs={'name': 'og:image'}))
    if og_image:
        for img in og_image:
            if validators.url(str(img['content'])):
                images += [img['content']]
    thumbnail_spec = soup.findAll('link', rel='image_src')
    if thumbnail_spec:
        for img in thumbnail_spec:
            if validators.url(str(img['href'])):
                images += [str(img['href'])]
    for img in imagez:
        if "sprite" not in img["src"]:
            if validators.url(str(img['src'])):
                images += [str(img["src"])]
    return images
    
    
    
    
@app.route("/secure-page")
def secure_page():
    return render_template('thumbnails.html')
    
@app.route("/logout")
def logout():
    #logout_user()
    flash("Successfully Logged out")
    return redirect(url_for("home"))
        


###

# The functions below should be applicable to all Flask apps.

###



@app.route('/<file_name>.txt')

def send_text_file(file_name):

    """Send your static text file."""

    file_dot_text = file_name + '.txt'

    return app.send_static_file(file_dot_text)





@app.after_request

def add_header(response):

    """

    Add headers to both force latest IE rendering engine or Chrome Frame,

    and also to tell the browser not to cache the rendered page.

    """

    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'

    response.headers['Cache-Control'] = 'public, max-age=0'

    return response





@app.errorhandler(404)

def page_not_found(error):

    """Custom 404 page."""

    return render_template('404.html'), 404





if __name__ == '__main__':

    app.run(debug=True,host="0.0.0.0",port="8080")