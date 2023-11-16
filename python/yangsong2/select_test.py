import pymysql
import os

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="1q2w3e4r!",
    db="testtest",
    charset="utf8mb4",
    autocommit=True,
    cursorclass=pymysql.cursors.DictCursor,
)
cur = conn.cursor()
sql = "select * from area where content = %s"
cur.execute(sql, "듣기·말하기")
res = cur.fetchall()
for r in res:
    print(r)