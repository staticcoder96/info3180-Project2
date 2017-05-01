"""

Flask Documentation:     http://flask.pocoo.org/docs/

Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/

Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.

"""
import os
from app import app,db
from app.models import Profile,Wishlist,Item
from flask import render_template, request, redirect, url_for, flash,jsonify,make_response,session
from flask_login import logout_user, login_required
from flask_jwt import JWT, jwt_required, current_identity
from bs4 import BeautifulSoup
from .forms import WishForm, LoginForm, SignUpForm,ShareForm
import validators
import requests
import urlparse   
import smtplib
from werkzeug.utils import secure_filename
                                                             




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
       # file_folder =  app.config['UPLOAD_FOLDER']
        
        if form.validate_on_submit() and request.method == 'POST':
            
            #check that the inputs are correct
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            #image = form.image.data
            
            
            #get picture
            #pic = request.files['image']
            #image = secure_filename(pic.filename)
            #pic.save(os.path.join(file_folder, image))
            
            #save information to database
            user = Profile(username,password,email,first_name,last_name)
            userid=user.id
            db.session.add(user)
            db.session.commit()
            if user!=None:
                flash("User Successfully Added")
                return redirect(url_for('login')) #brings users to login page page
        


@app.route("/api/users/login", methods=["GET", "POST"])
def login():
    """Accepts login credentials as username and password
    """
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            passw = form.password.data
            
            authenticate(email,passw)
            
        if form.email.data and form.password.data:
            user=db.session.query(Profile).filter_by(email=email, password=passw).first()
            # get user id, load into session
            userid=user.id
            #login_user(user)
            if user!=None:
                db.session.add(user)
                db.session.commit()
                flash("Logged in Successfully")
                response = jsonify({"error":"null","data":{'id':user.id,'username':user.username},"message":"logged"})
                return redirect(url_for('wishhome',userid=user.id))
            else:

                response = jsonify({"error":"1","data":{},"message":'not logged'})
                return render_template("login.html", form=form) #they should be redirected to their page or wishlist
    return render_template("login.html", form=form)

@app.route("/api/users/<int:userid>/wishlist/", methods=["GET","POST"])
#@login_required

def wishhome(userid):
    if request.method == 'GET':
        """Returns a users wishlist based on their user id
        """
        form=WishForm()
        sheet=ShareForm()
        user2=db.session.query(Profile).filter_by(id=userid).first()
        user=db.session.query(Wishlist).filter_by(userid=userid)
        return render_template("wishlist.html",wish=user,user=user2,form=form,sheet=sheet)
    
    if request.method == 'POST':
        """Add items to the wishlist
        """
        form=WishForm()
        sheet=ShareForm()
        title = form.title.data
        description = form.description.data
        url = form.url.data
        wishl = Item(userid,title,description,url)
        db.session.add(wishl)
        db.session.commit()
        flash("ITEM SUCCESSFULLY ADDED")
        #share_wishlist(email)
        #return redirect(url_for('wishhome',userid=userid,form=form))
        return redirect(url_for('thumbnail',url=url,form=form,wishid=wishl.id,sheet=sheet))
    else:
        flash("ITEM UNSUCCESSFULLY ADDED")
        return render_template("wishlist.html",wish=user,user=userid,form=form,sheet=sheet)
        

    
@app.route("/api/users/{userid}/wishlist/{itemid}",methods=['GET','POST','DELETE'])
#@login_required

def wishno(userid,itemid):
    """Deletes an item from a users wishlist
    """
    if request.method == "POST":
        """delete the item from the wishlist
        """
        form=WishForm()
        title = form.title.data
        description = form.description.data
        url = form.url.data
        wishl = Item(userid,description,title,url)
        db.session.delete(wishl)
        db.session.commit()
        
        flash("Item Successfully Deleted")
    else:
        flash("Item Unsuccessfully Deleted")
        return redirect(url_for("wishlist.html"))
    return render_template("wishlist.html",userid=userid,itemid=itemid)

@app.route("/api/users/<int:userid>/wishlist/share",methods=['GET','POST'])
#@login_required

def share_wishlist(userid):
    """Share the wishlist"""
    sheet=ShareForm()
    if request.method == "POST":
        email = sheet.email.data
        sendmail(email) #share the wishlist
        flash("E-Mail SENT!!")
        return redirect(url_for("wishhome",userid=userid,sheet=sheet))
    else:
        flash("E-MAIL NOT SENT") 
        return render_template("wishlist.html",userid=userid,sheet=sheet)

def sendmail(email):
    """Sends the link of your wishlist to your friends or family
    """
    from_addr = 'stephanieramsay6@gmail.com'
    to_addr = email
    
    Subject = "This is the link to my wishlist"
    message = "<b> <a href={{ url_for('wishhome') }}>Wishlist</a> </b>"
    
    username = 'securesally@gmail.com'
    password = 'cxqu xawu hiyq qphm'
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(from_addr, password)
    
    BODY = '\r\n'.join(['To: %s' %to_addr,
        'From: %s' %from_addr,
        'Subject: %s' %Subject,
        '',
        message
        ])
    try:
        server.sendmail(from_addr, [to_addr], BODY)
        print 'EMAIL SENT'
    except:
        print 'ERROR Sending Email'
        
    server.quit()
    
    


@app.route('/api/<int:wishid>/thumbnail/', methods=["GET","POST"])
def thumbnail(wishid):
    urlz=db.session.query(Item).filter_by(id=wishid).first()
    if urlz.item_url == "" or not validators.url(urlz.item_url):
        response = jsonify({"error": "1","thumbnails":[],"message": "Unable to extract thumbnails"})
    else:
       # thumbnails = {'':get_images(url)}
       
       response=get_images(urlz.item_url)
       #response=jsonify(error='Null',thumbnails=get_images(urlz.item_url), message="Success")
       return render_template("thumbnails.html",res=response,too="tiger")
   return render_template("thumbnails.html",res=response,too="tiger")
       
        
        
def get_images(url):
    images = []
    soup = BeautifulSoup(requests.get(url).text,"html.parser")
    imagez =soup.findAll("img",src=True)
    og_image = (soup.find('meta', property='og:image') or
                        soup.find('meta', attrs={'name': 'og:image'}))
    if og_image and og_image['content']:
        images.append(og_image['content'])
#for img in og_image:if validators.url(str(img['content'])):images += [img['content']]

    thumbnail_spec = soup.find('link', rel='image_src')
    
    if thumbnail_spec and thumbnail_spec['href']:
        images.append(thumbnail_spec['href'])
    
    image = '%s'
    
    for img in soup.findAll('img', src=True):
        images.append(image % urlparse.urljoin(url, img['src']))
    return images
    
    """
        for img in thumbnail_spec:
            if validators.url(str(img['href'])):
                images += [str(img['href'])]
    for img in imagez:
        if "sprite" not in img["src"]:
            if validators.url(str(img['src'])):
                images += [str(img["src"])]
    return images"""
    
    
    
    
@app.route("/secure-page")
def secure_page():
    return render_template('thumbnails.html')
    
@app.route("/logout")
def logout():
    #logout_user()
    flash("Successfully Logged out")
    return redirect(url_for("home"))
    

def authenticate(email,password):
    """JWT Authentication Header
    """
    #app.config['SECRET_KEY']='shh..itsasecret'
    secret='shh..itsasecret'
    #header
    header = {
        "alg":"HS256",
        "typ":"JWT"
        }
        
    #payload
    payload = {
        "email":email,
        "password":password
    }
    #HMACSHA256
    
    #signature = HMACSHA256(
    #    base64UrlEncode(header) + "." + base64UrlEncode(payload),
     #   secert
     #   )
   # 
   # print 'Authorization: Bearer' + "<" + signature +"."+ result +">"
    
    
    
##

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