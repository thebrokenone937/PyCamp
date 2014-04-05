from sqlalchemy import *
from ..base import Base
from ..service import Service
from flask.ext.login import LoginManager, UserMixin
from project import app


login_manager = LoginManager()
login_manager.init_app(app) 


class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    email = Column(String(100))
    password = Column(String(255))
    salt = Column(String(255))
    role_id = Column(Integer)
    forgot_password_hash = Column(String(255))
    
    def __init__(self, id=0, username="", email="", password="", salt="", role_id=0, forgot_password_hash="", active=False):
        self.username = username
        self.id = id
        self.active = active
        self.role_id = role_id
        self.email = email
        self.salt = salt
        self.forgot_password_hash = forgot_password_hash
        self.password = password
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_role_id(self):
        return self.role_id
    
    def __repr__(self):
        return '<User %r>' % (self.username)
    
    
    
class UsersService(Service):
    Model = Users
    
@login_manager.user_loader
def load_user(id):
    # 1. Fetch against the database a user by `id` 
    # 2. Create a new object of `User` class and return it.
    usersService = UsersService()
    u = usersService.first(id=int(id))
    if u:
        return Users(username=u.username, id=u.id, active=True, role_id=u.role_id)
    else:
        return None
