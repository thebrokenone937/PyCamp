from sqlalchemy import *
from ..base import Base
from ..service import Service

class TodoAssignedUsers(Base):
    __tablename__ = 'todo_assigned_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    todo_id = Column(Integer)
    
class TodoAssignedUsersService(Service):
    Model = TodoAssignedUsers 