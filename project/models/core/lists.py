from sqlalchemy import *
from ..base import Base
from ..service import Service
from project.models.engine import *
from project.models.core.todos import Todos

class Lists(Base):
    __tablename__ = 'lists'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    project_id = Column(Integer)
    due_date = Column(DateTime)
    created = Column(DateTime)
    completion_date = Column(DateTime)
    status = Column(Enum('Open','Closed'))
    priority_level = Column(Integer)
    user_id = Column(Integer)
    is_del = Column(Integer)
    
class ListsService(Service):
    Model = Lists 
    
    def get_list_items(self, listId):
        return session.query(Lists, Todos).\
                     filter(Todos.list_id==Lists.id).\
                     filter(Todos.is_del==0).\
                     filter(Lists.id==listId).\
                     all()
