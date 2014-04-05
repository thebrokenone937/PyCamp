import yaml
from flask import Flask, Blueprint
#import os
from flask.ext.login import LoginManager
#from flask.ext.openid import OpenID
#from config import basedir
from beaker.middleware import SessionMiddleware
import sys

test_mode = False

try:
    if sys.argv[1] == 'test':
        test_mode = True
except:
    test_mode = False
 

session_opts = {
    'session.type': 'file',
    'session.data_dir': './cache',
}

app = Flask(__name__)

stream = file('project/modules.yml', 'r')
modules = yaml.load_all(stream)

# Import modules
for module in modules:

    print module
    #continue
    # Get module name from 'url' setting, exculde leading slash
    modname = module['url'][1:]

    try:
        # from project.controllers.<modname> import <modname>
        mod = __import__(
            'project.controllers.' + modname, None, None, modname
        )
    except Exception as e: print e
        # Log exceptions here
        # [...]
    
    mod = getattr(mod, modname)  # Get blueprint from module
    
    app.register_blueprint(mod)

app.secret_key = 'dantest'     
app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts) 
app.debug = True
app.run(use_debugger=False, debug=True, use_reloader=False, host='127.0.0.1')
