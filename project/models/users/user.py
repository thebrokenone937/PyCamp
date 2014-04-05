from sqlalchemy import *

def initDb():
    db = create_engine('mysql+mysqldb://')

    db.echo = False  # Try changing this to True and see what happens

    metadata = MetaData(db)

    users = Table('members', metadata, autoload=True)

    s = users.select(users.c.username == 'TheBrokenOne')
    rs = s.execute()

    row = rs.fetchone()
    print 'Id:', row[0]
    print 'Name:', row['username']
    print 'Email:', row.email
    print 'Password:', row[users.c.password]

    for row in rs:
        print row.username, 'email is', row.email