from sqlalchemy import *
from ..base import Base
from ..service import Service


class Drawings(Base):
    __tablename__ = 'drawings'
    
    id= Column(Integer, primary_key=True)
    user_id= Column(Integer)
    edit_id= Column(Integer)
    type_id= Column(Integer)
    background_image_id= Column(Integer)
    url= Column(String(255))
    title= Column(String(255))
    thumb_url= Column(String(255))
    image_url= Column(String(255))
    gzip_url= Column(String(255))
    created= Column(DateTime)
    verified= Column(Integer)
    public= Column(Integer)
    mature= Column(Integer)
    flags= Column(Integer)
    likes= Column(Integer)
    dislikes= Column(Integer)
    views= Column(Integer)
    ip= Column(Integer)
    timetaken= Column(Time)
    frames= Column(Integer)
    lines= Column(Integer)
    canvas_color= Column(String(6))
    score= Column(Integer)
    num_comments= Column(Integer)
    num_favourites= Column(Integer)
    original_edit_id= Column(Integer)
    version= Column(Integer)
    category_id= Column(Integer)
    comment_status= Column(Integer)
    width= Column(Integer)
    height= Column(Integer)
    
    
class DrawingsService(Service):
    #pass
    Model = Drawings