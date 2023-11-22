from flask import Flask, render_template
import mysql.connector
import serial
import time

app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

mydb = mysql.connector.connect(
  host="localhost",
  user="farmer1",
  password="1q2w3e4r",
  database="yangsongfarm"
)

@app.route('/')
def index():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        data = line.split("\t")
        if len(data) >=2: #데이터가 적어도 2개의 부분으로 구성되어 있는지 확인
            # % 기회 제거 후 부동소수점 숫자로 변환
            humidity_str = data[0].split(": ")[1].replace('%', '')
            humidity = float(humidity_str)
            # 비슷한 방법으로 온도 데이터 처리
            temperature_str = data[1].split(": ")[1].replace(' *C', '')
            temperature = float(temperature_str)

            #데이터베이스에 데이터 삽입
            mycursor = mydb.cursor()
            sql = "INSERT INTO readings (humidity, temperature) VALUES (%s, %s)"
            val = (humidity, temperature)
            mycursor.execute(sql, val)
            mydb.commit()

            return render_template('index.html', humidity=humidity, temperature=temperature)
        else:
            print("데이터가 없음")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

