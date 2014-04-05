from sqlalchemy import *
from ..base import Base
from ..service import Service

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    list_id = Column(Integer)
    due_date = Column(DateTime)
    created = Column(DateTime)
    completion_date = Column(DateTime)
    status = Column(Enum('Open','Closed'))
    priority_level = Column(Integer)
    user_id = Column(Integer)
    is_del = Column(Integer)
    
class TodosService(Service):
    Model = Todos 