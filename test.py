import datetime
import mysql.connector

cnx = mysql.connector.connect(user='admin', database='askme', password='Welcome#1', host='10.0.1.216')
cursor = cnx.cursor()

query = ("select 1")

cursor.execute(query)

for test in cursor:
    print(test)

cursor.close()
cnx.close()
