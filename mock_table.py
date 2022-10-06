import sqlite3

# Connect to database test.sqlite
conn = sqlite3.connect("test.sqlite")

#Clear all data
try:
	conn.execute("""DROP TABLE files;""")
except: pass
try:
	conn.execute("""DROP TABLE users;""")
except: pass
# Create table Files
conn.execute("""CREATE TABLE FILES(
FileID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
NAME VARCHAR NOT NULL,
TYPE VARCHAR NOT NULL,
PATH VARCHAR NOT NULL,
UserID INTEGER NOT NULL,
FOREIGN KEY(UserID) REFERENCES USERS(UserID)
);""")

# Create table Users
conn.execute("""CREATE TABLE USERS(
UserID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
USERNAME VARCHAR NOT NULL,
PASSWORD VARCHAR NOT NULL
);""")

# Close connection
conn.close()