from flask import Blueprint, render_template, abort
import project.models.generator.generator as generator
from project.models.core.drawings import DrawingsService
#from project.models import *

# Module name is 'user', thus save Blueprint as 'user' variable
user = Blueprint('user', __name__)

"""drawingsService = DrawingsService()
    
record = drawingsService.first(title='test drawing')

drawingsService.update(record, title='test drawing update')

print record.url, record.image_url
"""

@user.route('/user')
def index():
    generator.getTables()
    #drawings = Drawings()
    
    #result = session.query(Drawings).filter_by(title='test drawing').first() 
    """drawingsService = DrawingsService()
    
    result = drawingsService.getByColumn(title='test drawing')
    
    print result.url, result.image_url"""
    return 'Testing'