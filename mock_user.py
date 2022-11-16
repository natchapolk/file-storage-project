import os
import sqlite3
dir_path = os.path.dirname(os.path.realpath(__file__))
#Create files folder
try: os.mkdir("files")
except: print("Files folder exist.")
# Connect to database
conn = sqlite3.connect("test.sqlite")
#Get user and password list
f = open("users.txt", "r")
data = f.read()
f.close()
data = data.split("\n")
for user in data:
	user = user.split("\t")
	print(user[0]+" "+user[1])
	#create folder
	try: os.mkdir("files/"+user[0])
	except: print("Folder exist")
	#Add user and password to database
	conn.execute("INSERT INTO USERS(USERNAME, PASSWORD) VALUES ('"+user[0]+"', '"+user[1]+"');")
conn.commit()
# Close connection
conn.close()