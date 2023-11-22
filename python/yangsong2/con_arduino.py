#from black import E
import serial
import re
import json
import pymysql

conn = pymysql.connect(
    host="127.0.0.1", user="song1", password="1q2w3e4r", db="yangsong2", charset="utf8"
)
cur = conn.cursor()

#ser = serial.Serial(port="COM5", baudrate=9600)
ser = serial.Serial(port="/dev/ttyACM0", baudrate=9600)

p = re.compile("{.+}")

i = 0
while True:
    if ser.readable():
        res = ser.readline()
        s = res.decode()[: len(res) - 1]
        if p.match(s):
            print("test")
            try:
                j = json.loads(s)
                print(f"sucess: {j}")
                cur.execute(
                    f"INSERT INTO yang{j['id']} (co2, temperature, humidity) VALUES ({j['co2']}, {j['temperature']}, {j['humidity']})"
                )

                conn.commit()
            except Exception as e:
                print(f"error: {s}")
                print(f"error message: {e}")
        i += 1
