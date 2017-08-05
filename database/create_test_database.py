""" Creating a test db before the real run"""
import sqlite3

SQL_ORIG = r"./vocab.db"
SQL_REPL = r"./test.db"

vocab_list = []
with sqlite3.connect(SQL_ORIG) as connection:
    c = connection.cursor()
    c.execute("SELECT vocab FROM pho;")
    raw_list = c.fetchall()

vocab = [item[0] for item in raw_list]

with sqlite3.connect(SQL_REPL) as connection:
    c = connection.cursor()
    for item in vocab:
        c.execute("INSERT INTO pho (vocab) VALUES (?);", (item,))
    
