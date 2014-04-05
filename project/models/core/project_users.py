from sqlalchemy import *
from ..base import Base
from ..service import Service
from project.models.engine import *
from project.models.core.users import Users

class ProjectUsers(Base):
    __tablename__ = 'project_users'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer)
    user_id = Column(Integer)
    
class ProjectUsersService(Service):
    Model = ProjectUsers
    
    def get_project_users(self, projectId):
        return session.query(ProjectUsers, Users).\
                     filter(ProjectUsers.user_id==Users.id).\
                     filter(ProjectUsers.project_id==projectId).\
                     all() 