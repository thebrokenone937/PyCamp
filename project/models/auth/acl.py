from sqlalchemy import *
from ..base import Base
from ..service import Service

class Acl(Base):
    __tablename__ = 'acl'
    
    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    
class AclService(Service):
    Model = Acl    
    