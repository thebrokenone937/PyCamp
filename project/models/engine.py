from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+mysqldb://<username>:<password>@<host>/<database_name>')
Session = sessionmaker(bind=engine)
session = Session()
