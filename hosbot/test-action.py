import sqlite3

conn = sqlite3.connect('hospital.db')
dictionary = {"mangalore" : 1, "panaji" : 2, "jaipur" : 3, "salem" : 4, "vijayawada" : 5}
hid = dictionary["Mangalore".lower()]
speciality = "Urology"
cursor = conn.execute("SELECT DNAME, DFEE FROM DOCTOR WHERE HID = " + str(hid) + " AND DSPECIAL = \"" + speciality + "\"")
data = cursor.fetchall()
if len(data) == 0:
	speech = "No doctors available for the given input."
else: 
	speech = "#\tDoctor Name\t\tFee\n"
	i=1
	for name, fee in data:
		speech = speech + str(i) + "\t" + name + "\t" + str(fee) + "\n"
		i+=1
print speech

conn.close()