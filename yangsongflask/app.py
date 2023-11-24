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
        print(f"Raw Serial Data:{line}") # 원시 시리얼 데이터 로그
        data = line.split("\t")
        print(f"Parased Data: {data}") # 파싱된 데이터로그
        print(len(data))
        if len(data) >= 3:
            humidity_str = data[0].split(": ")[1].replace('%', '')
            temperature_str = data[1].split(": ")[1].replace(' *C', '')
            co2_str = data[2].split(": ")[1].replace(' ppm', '') # 새로 추가된 부분
        else:
            print("Data does not have enough elements")
        return float(humidity_str), float(temperature_str), float(co2_str)
    return None, None, None # 수정된 반환 값

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ys2_data')
def ys2_data():
    humidity, temperature, co2 = read_serial_data() # CO2 추가
    if humidity is not None and temperature is not None and co2 is not None:
        try:
            mycursor = mydb.cursor()

            # 행 수 확인
            mycursor.execute("SELECT COUNT(*) FROM readings")
            count = mycursor.fetchone()[0]
            if count >=6920:
                mycursor.execute("DELETE FROM readings ORDER BY timestamp ASC LIMIT 1")
                print(f"Delete log") # 데이터 제거
            sql = "INSERT INTO readings (humidity, temperature, co2) VALUES (%s, %s, %s)"
            val = (humidity, temperature, co2)
            print(f"Executing SQL: {sql} with values {val}") # SQL 실행 로그
            mycursor.execute(sql, val)
            mydb.commit()
            print(f"Inserted data into database") # 데이터 삽입 확인 로그
            mycursor.close()
        except mysql.connector.Error as err:
            print(f"Error occurred: {err}") # 예외 발생 시 로그 출력

    mycursor = mydb.cursor(dictionary=True)
    # CO2 데이터를 포함하여 쿼리 실행
    mycursor.execute("SELECT timestamp, temperature, humidity, co2 FROM readings ORDER BY timestamp DESC LIMIT 10")
    data = mycursor.fetchall()
    #print(f"Retrieved data: {data}") # 조회된 데이터 로그
    mycursor.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

