import psycopg2
import sys

# Drop all tables from a given database

try:
    conn = psycopg2.connect("dbname='seipetali_prod' user='seipetali_prod' password='DvoGS9W1jEDhdTD' host='localhost' ")
    conn.set_isolation_level(0)
except:
    print "Unable to connect to the database."

cur = conn.cursor()

try:
    cur.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")
    rows = cur.fetchall()
    for row in rows:
        print "dropping table: ", row[1]   
        cur.execute("drop table " + row[1] + " cascade") 
    cur.close()
    conn.close()        
except:
    print "Error: ", sys.exc_info()[1]
