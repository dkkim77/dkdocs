# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 11:25:10 2018

@author: KDK

SQLite3 Python Type
NULL    None
INTEGER int
REAL    float
TEXT    str, bytes
BLOB    buffer
"""

import sqlite3

con = sqlite3.connect("test.db") # 메모리상 DB 생성시 : connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE PHONE_BOOK(NAME, PHONE_NUM);")
cur.execute("INSERT INTO PHONE_BOOK VALUES('KMK', '010-1234-5678');")
cur.execute("INSERT INTO PHONE_BOOK VALUES('KDK', '010-9761-5678');")

sql = "INSERT INTO PHONE_BOOK VALUES(?, ?);"
datalist = (('LSJ', '010-6215-1234'), ('LEE','010-2222-1234'))
cur.executemany(sql, datalist)
con.commit()    # AutoCommit mode : con.isolation_level = None

cur.execute("SELECT * FROM PHONE_BOOK;")
for row in cur:
    print(row)

cur.close()
con.close()
