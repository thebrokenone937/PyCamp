from sqlalchemy import *
from ..base import Base
from ..service import Service
from project.models.engine import *
from project.models.core.users import Users

class Files(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    comment_id = Column(Integer)
    url = Column(String(255))
    is_del = Column(Integer)
    name = Column(String(255))
    todo_id = Column(Integer)
    list_id = Column(Integer)
    project_id = Column(Integer)
    
class FilesService(Service):
    Model = Files
    
    def get_project_files(self, projectId, limit):
        return session.query(Files, Users).\
                     filter(Files.user_id==Users.id).\
                     filter(Files.project_id==projectId).\
                     order_by(desc(Files.id)).limit(limit)     