from sqlalchemy import *
from ..base import Base
from ..service import Service


class Friends(Base):
    __tablename__ = 'friends'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    friend_id = Column(Integer)
    
class FriendsService(Service):
    Model = Friends 