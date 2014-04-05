from sqlalchemy import *
from ..base import Base
from ..service import Service

class Roles(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    role = Column(String(255))
    
class RolesService(Service):
    Model = Roles    
    