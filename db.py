import sqlite3

# Select
def select(value: str, table: str, where: str = ""):
	conn = sqlite3.connect("test.sqlite")
	if where != "":
		cursor = conn.execute("SELECT "+value+" FROM "+table+" WHERE "+where+";")
	else:
		cursor = conn.execute("SELECT "+value+" FROM "+table+";")
	data = []
	for i in cursor:
		l = []
		for j in i:
			l.append(j)
		data.append(l)
	conn.close()
	return data

# insert data
def insert(table: str, column: str, value: str):
	conn = sqlite3.connect("test.sqlite")
	conn.execute("INSERT INTO "+table+"("+column+")values("+value+");")
	conn.commit()
	conn.close()
	return "Value inserted"

#Update
def update(table: str, value: str, where: str):
	conn = sqlite3.connect("test.sqlite")
	conn.execute("UPDATE "+table+" SET "+value+" WHERE "+where+";")
	conn.commit()
	conn.close()
	return "Value updated"

#delete
def delete(table: str, where: str):
	conn = sqlite3.connect("test.sqlite")
	conn.execute("DELETE FROM "+table+" WHERE "+where+";")
	conn.commit()
	conn.close()
	return "Value deleted"