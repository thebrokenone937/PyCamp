from sqlalchemy import *
from ..base import Base
from ..service import Service
from project.models.engine import *
from project.models.core.project_users import ProjectUsers
from project.models.core.lists import Lists
from project.models.core.todos import Todos
from project.models.core.todo_assigned_users import TodoAssignedUsers

class Projects(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    due_date = Column(DateTime)
    created = Column(DateTime)
    completion_date = Column(DateTime)
    status = Column(Enum('Open','Closed'))
    priority_level = Column(Integer)
    user_id = Column(Integer)
    is_del = Column(Integer)
    
class ProjectsService(Service):
    Model = Projects
    
    def get_projects(self, userId):
        return session.query(ProjectUsers, Projects).\
                     filter(Projects.id==ProjectUsers.project_id).\
                     filter(ProjectUsers.user_id==userId).\
                     all()

               
    def get_user_items(self, userId):
        return session.query(Projects, Lists, Todos, TodoAssignedUsers).\
                     filter(Projects.id==Lists.project_id).\
                     filter(Todos.list_id==Lists.id).\
                     filter(Todos.id==TodoAssignedUsers.todo_id).\
                     filter(TodoAssignedUsers.user_id==userId).\
                     filter(Todos.is_del==0).\
                     all()
    
    def get_project_items(self, projectId):
        return session.query(Projects, Lists, Todos).\
                     filter(Projects.id==Lists.project_id).\
                     filter(Todos.list_id==Lists.id).\
                     filter(Projects.id==projectId).\
                     filter(Todos.is_del==0).\
                     all()


    def get_list_items(self, listId):
        return session.query(Lists, Todos).\
                     filter(Lists.id==listId).\
                     filter(Todos.list_id==Lists.id).\
                     filter(Todos.is_del==0).\
                     all()
