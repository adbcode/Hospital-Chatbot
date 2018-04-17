import sqlite3

conn = sqlite3.connect('hospital.db')
name = "Aditya B"
age = "20"
sex = "M"
cursor = conn.execute("SELECT PID FROM PATIENT WHERE PNAME = \"" + name + "\" AND PAGE = " + age + " AND PSEX = \"" + sex + "\"")
data = cursor.fetchall()
print data
if len(data) == 0:
	cursor = conn.execute("INSERT INTO PATIENT (PNAME, PAGE, PSEX) VALUES (\'" + name + "\', " + age + ", \'" + sex + "\')")
	cursor = conn.execute("SELECT PID FROM PATIENT WHERE PNAME = \"" + name + "\" AND PAGE = " + age + " AND PSEX = \"" + sex + "\"")
	data = cursor.fetchone()
	speech = "New patient profile created. Your patient id is: " + str(data[0]) + "."
else: 
	speech = "Profile already exists. Your patient id is: " + str(data[0][0]) + "."
print("Response:")
print(speech)

cursor = conn.execute("SELECT * FROM PATIENT WHERE PNAME = \"" + name + "\" AND PAGE = " + age + " AND PSEX = \"" + sex + "\"")
data = cursor.fetchall()
print data

conn.commit()
conn.close()