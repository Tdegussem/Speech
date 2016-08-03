import MySQLdb
import time

db = MySQLdb.connect(host="sql7.freemysqlhosting.net", user="sql7129980", passwd="zexEhCxu1G", db="sql7129980")
#create a cursor for the select
cur = db.cursor()



# Prepare SQL query to INSERT a record into the database.
sql = """INSERT INTO `sql7129980`.`speech` (`NAME`, `SPEED`, `DATE`) VALUES ('Gert', '100', CURRENT_TIMESTAMP);"""
cur.execute(sql)
   # Commit your changes in the database
db.commit()
#try:
   # Execute the SQL command
   #cursor.execute(sql)
   # Commit your changes in the database
   #db.commit()
#except:
   # Rollback in case there is any error
   #db.rollback()

uptime = 0
starttime = time.time()
print starttime

while 1:
    sql = """INSERT INTO `sql7129980`.`Slaves` (`ID`, `IP`, `UP`, `TIME`) VALUES ('1', '192.168.1.3', """ +str(uptime) +""", CURRENT_TIMESTAMP +3600);"""
 
    uptime = round(time.time() - starttime,0)
    print uptime
    time.sleep(5)
    cur.execute(sql)
    db.commit()
    


# disconnect from server
db.close()
