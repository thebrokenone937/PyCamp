from sqlalchemy import *
from ..base import Base
from ..service import Service

class PriorityLevels(Base):
    __tablename__ = 'priority_levels'

    id = Column(Integer, primary_key=True)
    priority = Column(String(255))
    
class PriorityLevelsService(Service):
    Model = PriorityLevels 