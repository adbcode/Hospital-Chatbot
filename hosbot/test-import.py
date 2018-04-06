import sqlite3

conn = sqlite3.connect('hospital.db')

cursor = conn.execute("SELECT * from MEDICINE")
for row in cursor:
	print row
	#print "DFEE = ", row[4], "\n"

conn.close()