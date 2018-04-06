import sqlite3
import csv

f=open('medicine.csv','r') # open the csv data file
#next(f, None) # skip the header row
reader = csv.reader(f)

conn = sqlite3.connect('hospital.db')
cur = conn.cursor()
			 
for row in reader:
	cur.execute("INSERT INTO MEDICINE VALUES (?, ?, ?, ?, ?)", row)
	
f.close()
conn.commit()
conn.close()