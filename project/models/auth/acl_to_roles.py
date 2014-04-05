from sqlalchemy import *
from ..base import Base
from ..service import Service

class AclToRoles(Base):
    __tablename__ = 'acl_to_roles'
    
    id = Column(Integer, primary_key=True)
    acl_id = Column(Integer)
    role_id = Column(Integer)
    
class AclToRolesService(Service):
    Model = AclToRoles    
    