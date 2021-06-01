# this is a file to cleare the db, delete a table and then re create the table

import sqlite3
conn = sqlite3.connect('users.db')
try:
    conn.execute('''DROP TABLE USERS;''')
except:
    pass

conn.execute('''CREATE TABLE USERS
 ( EMAIL   TEXT  PRIMARY KEY    NOT NULL,
 UPDATE_DATE            TEXT     NOT NULL,
 DAY_GAP INT
 
 );''')

cursor = conn.cursor()

tuple1 = ['checker@checcker', '2021-01-01', 1]
insert_query = """REPLACE INTO USERS (EMAIL,UPDATE_DATE,DAY_GAP) VALUES (? , ? , ?)"""
cursor.execute(insert_query, tuple1)
conn.commit()

conn.close()