from sqlalchemy import *
from ..base import Base
from ..service import Service
from project.models.engine import *
from project.models.core.users import Users
from project.models.core.todos import Todos
from project.models.core.lists import Lists

class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    todo_id = Column(Integer)
    comment = Column(Text)
    created = Column(DateTime)
    user_id = Column(Integer)
    is_del = Column(Integer)
    
class CommentsService(Service):
    Model = Comments
    
    def get_comments(self, todoId):
        return session.query(Comments, Users).\
                     filter(Comments.user_id==Users.id).\
                     filter(Comments.todo_id==todoId).\
                     filter(Comments.is_del==0).\
                     all()
                     
    def get_project_comments(self, projectId, limit):
        return session.query(Todos, Comments, Users, Lists).\
                     filter(Comments.user_id==Users.id).\
                     filter(Comments.todo_id==Todos.id).\
                     filter(Todos.list_id==Lists.id).\
                     filter(Lists.project_id==projectId).\
                     filter(Comments.is_del==0).\
                     order_by(desc(Comments.created)).limit(limit)
                     
    def get_num_comments(self, todoId):
        return session.query(Comments).\
                     filter(Comments.is_del==0).\
                     filter(Comments.todo_id==todoId).count()