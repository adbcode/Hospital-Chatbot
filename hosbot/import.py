import sqlite3
import csv

f=open('doctor.csv','r') # open the csv data file
#next(f, None) # skip the header row
reader = csv.reader(f)

conn = sqlite3.connect('hospital.db')
cur = conn.cursor()
			 
for row in reader:
	cur.execute("INSERT INTO DOCTOR VALUES (?, ?, ?, ?, ?)", row)
	
f.close()
conn.commit()
conn.close()