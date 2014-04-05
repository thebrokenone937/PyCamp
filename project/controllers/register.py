from flask import Blueprint, render_template, abort, request
from project.models.core.users import UsersService
from project import app
from project.lib.template import render_custom_template, isTokenValid
import flask
from flaskext.bcrypt import Bcrypt

register = Blueprint('register', __name__)

"""username = 'Dan'
email = ''
password = 'test'

usersService = UsersService()
    
emailResult = usersService.first(email=email)

print emailResult.email

bcrypt = Bcrypt(app)
"""

@register.route('/register')
def index():
    return render_custom_template('register/index.html')

@register.route('/register/register', methods=["POST"])
def register_action():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    password2 = request.form["password2"]
    token = request.form["token"]
    
    print email
    
    usersService = UsersService()
    
    if username:
        usernameResult = usersService.first(username=username)
    else:
        usernameResult = False
        
    if email:    
        emailResult = usersService.first(email=email)
    else:
        emailResult = False
        
    #do validation checking
    if not username:
        error = 'Please enter a username'
    elif usernameResult:
        error = 'Username has been taken'
    elif not email:
        error = 'Please enter an email address'
    elif emailResult:
        error = 'Email address has been taken'
    elif not password:
        error = 'Please enter a password'
    elif password != password2:
        error = 'Passwords do not match'
    elif not isTokenValid(token):
        error = 'The request did not come from Pycamp'    
    else:
        error = False
    
    #error = True
        
    if not error: 
        bcrypt = Bcrypt(app)
        pwHash = bcrypt.generate_password_hash(password)
           
        usersService.create(username=username, email=email, password=pwHash, salt='', role_id=2, forgot_password_hash='')
    
    return render_custom_template('register/index.html', error=error, username=username, email=email)
    