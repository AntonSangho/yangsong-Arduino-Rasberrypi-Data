from flask import Flask, render_template, jsonify
import mysql.connector
import serial
import time

app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

mydb = mysql.connector.connect(
  host="localhost",
  user="farmer1",
  password="1q2w3e4r",
  database="yangsongfarm"
)

def read_serial_data():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        data = line.split("\t")
        if len(data) >= 2:
            humidity_str = data[0].split(": ")[1].replace('%', '')
            temperature_str = data[1].split(": ")[1].replace(' *C', '')
            return float(humidity_str), float(temperature_str)
    return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ys2_data')
def ys2_data():
    humidity, temperature = read_serial_data()
    if humidity is not None and temperature is not None:
        mycursor = mydb.cursor()
        sql = "INSERT INTO readings (humidity, temperature) VALUES (%s, %s)"
        val = (humidity, temperature)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()

    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT timestamp, temperature, humidity FROM readings ORDER BY timestamp DESC LIMIT 10")
    data = mycursor.fetchall()
    mycursor.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

