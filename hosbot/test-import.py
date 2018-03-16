import sqlite3

conn = sqlite3.connect('hospital.db')

cursor = conn.execute("SELECT * from DOCTOR")
for row in cursor:
	print "DID = ", row[0]
	print "HID = ", row[1]
	print "DNAME = ", row[2]
	print "DSPECIAL = ", row[3]
	print "DFEE = ", row[4], "\n"

conn.close()