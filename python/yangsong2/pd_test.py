from dash import Dash, html, dcc
import pandas as pd
import pymysql
import datetime
from dash.dependencies import Output, Input

conn = pymysql.connect(
    host="127.0.0.1",
    user="song1",
    password="1q2w3e4r",
    db="yangsong2",
    charset="utf8",
    autocommit=True,
    cursorclass=pymysql.cursors.DictCursor,
)
cur = conn.cursor()

sql = f"select date_format(stamp,'%Y-%m-%d %H:%i') as stamp, ROUND(AVG(CO2), 2) as CO2 from yangsong2.yang1 WHERE DATE_FORMAT(stamp, '%Y-%m-%d')='2022-03-03' GROUP BY 1"
# sql = "INSERT INTO yang1 (co2, temperature, humidity) VALUES (600, 20, 10)"

cur.execute(sql)
result = cur.fetchall()
df = pd.DataFrame(result)
print(pd.to_datetime(df.stamp))
# print(df["date_format(stamp,'%Y-%m-%d %H:%i')"])