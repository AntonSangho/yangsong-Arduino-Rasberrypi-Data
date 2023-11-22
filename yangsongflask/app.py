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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ys2_data')
def ys2_data():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT timestamp, temperature, humidity FROM readings ORDER BY timestamp DESC LIMIT 10")
    data = mycursor.fetchall()
    mycursor.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

