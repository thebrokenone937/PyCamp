from flask import Blueprint, render_template, abort, request, session, redirect
from project.models.core.users import UsersService, load_user
from project import app
from project.lib.acl import check_acl
from project.models.core.login import validateResetForm
from project.lib.template import render_custom_template, isTokenValid
import flask
from flaskext.bcrypt import Bcrypt
from flask.ext.login import login_user, logout_user, current_user, login_required, current_user
import random
import smtplib
from email.mime.text import MIMEText

login = Blueprint('login', __name__)

@login.route('/login')
def index():
    return render_custom_template('login/login.html')

@login.route('/login/logout')
@check_acl('/login/logout')
def logout_action():
    logout_user()
    return render_custom_template('login/logout.html')

@login.route('/login/login', methods=["POST"])
def login_action():
    
    username = request.form["username"]
    password = request.form["password"]
    token = request.form["token"]
    
    usersService = UsersService()
    
    if username:
        usernameResult = usersService.first(username=username)
    else:
        usernameResult = False
        
    if not username:
        error = 'Please enter a username'
    elif not password:
        error = 'Please enter a password'
    elif not usernameResult:
        error = 'This user does not exist'
    elif not isTokenValid(token):
        error = 'The request did not come from Pycamp'
    else:
        error = False    
        
    if not error and usernameResult:    
        bcrypt = Bcrypt(app)
        if not bcrypt.check_password_hash(usernameResult.password, password):
            error = 'Invalid password entered'
        else:
            print 'logged in again'
            
            user = load_user(usernameResult.id)
            
            login_user(user)
            
            return redirect("/projects/list-projects")
            
            """session = request.environ['beaker.session']
            if not session.has_key('username'):
                session['username'] = username 
                session.save()   
                return "Session value set."
            else:
                return session['username'] """   
    
    return render_custom_template('login/login.html', error=error, username=username)


@login.route('/login/forgotPassword')
def forgot_password_action():
    return render_custom_template('login/forgot_password.html')
    
@login.route('/login/sendPassword', methods=["POST"])
def send_password_action():
    email = request.form["email"]
    token = request.form["token"]
    
    usersService = UsersService()
    
    if not email:
        error = 'Please enter an email address'
        emailResult = False
    else:
        emailResult = usersService.first(email=email)
        
        if not emailResult:    
            error = 'There is no account registerd with this email address'
        else:
            #generate hash
            hash = hex(random.getrandbits(128))[2:-1]
            #save hash to user record
            usersService.update(emailResult, forgot_password_hash=hash)
            #send mail with link
            error = 'Please go to the following url: http://127.0.0.1:5000/login/resetPassword?id=' + str(emailResult.id) + '&hash=' + str(hash)
            
            """
            msg = MIMEText('Please go to the following url: http://127.0.0.1:5000/login/resetPassword?hash=' + str(hash))
            msg['Subject'] = 'Forgot Password Link for PyCamp'
            msg['From'] = ''
            msg['To'] = emailResult.email
            
            # Send the message via our own SMTP server, but don't include the
            # envelope header.
            s = smtplib.SMTP('localhost')
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
            s.quit()"""
        
    return render_custom_template('login/forgot_password.html', email=email, error=error)  

@login.route('/login/resetPassword/<id>/<hash>', methods=["GET"])
def reset_password_form_action(id, hash):
    error = validateResetForm(id, hash)
    
    return render_custom_template('login/reset_password.html', id=id, hash=hash, error=error)

@login.route('/login/resetPasswordAction', methods=["POST"])
def reset_password_action():  
    hash = request.form["hash"]
    id = request.form["id"]
    password = request.form["password"]
    password2 = request.form["password2"]
    token = request.form["token"]
    
    error = validateResetForm(id, hash)
    
    if not error:
        if not password:
            error = 'Please enter a password'
        elif not password2:
            error = 'Please enter a password'
        elif password != password2:
            error = 'Passwords do not match'
        else:
            bcrypt = Bcrypt(app)
            pwHash = bcrypt.generate_password_hash(password)
            
            usersService = UsersService()
            userResult = usersService.first(id=int(id))
            
            usersService.update(userResult, password=pwHash)
            error = 'Password updated'
        
    return render_custom_template('login/reset_password.html', id=id, hash=hash, error=error)