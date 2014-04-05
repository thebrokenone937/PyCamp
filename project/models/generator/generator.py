from sqlalchemy import *
import re

def getTables():
    db = create_engine('mysql+mysqldb://')

    db.echo = False  # Try changing this to True and see what happens

    metadata = MetaData(db)

    sqlQuery = "SHOW tables"
    conn = db.connect()
    rs = conn.execute(sqlQuery)

    """row = rs.fetchone()
    print 'Id:', row[0]
    print 'Name:', row['username']
    print 'Email:', row.email
    print 'Password:', row[users.c.password]"""

    for row in rs:
        print "class " + row.Tables_in_pycamp + "(Base):"
        print "    __tablename__ = '" + row.Tables_in_pycamp + "'"
        print ""
        sqlQuery = "SHOW fields FROM " + row.Tables_in_pycamp
        fs = conn.execute(sqlQuery)
        
        for record in fs:
            length = re.search(r'\((.*)\)', record.Type)
            
            if "int(" in record.Type:
                print "    " + record.Field + "= Column(Integer)"
            elif "varchar(" in record.Type:
                print "    " + record.Field + "= Column(String(" + length.group(1) + "))"
            elif "char(" in record.Type:
                print "    " + record.Field + "= Column(String(" + length.group(1) + "))"
            elif "datetime" in record.Type:
                print "    " + record.Field + "= Column(DateTime)"
            elif "time" in record.Type:
                print "    " + record.Field + "= Column(Time)" 
            elif "text" in record.Type:
                print "    " + record.Field + "= Column(Text)"    
            elif "enum(" in record.Type:
                print "    " + record.Field + "= Column(Enum(" + length.group(1) + "))"
            else:
                print "    " + record.Field