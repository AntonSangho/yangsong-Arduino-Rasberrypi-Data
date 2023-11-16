from flask import Flask, render_template, abort, request, session
import os
import datetime
import pymysql

app = Flask(__name__)
app.secret_key = "1q2w3e4r"
app.permanent_session_lifetime = datetime.timedelta(minutes=5)
app.config["DEBUG"] = True

conn = pymysql.connect(
    host="127.0.0.1",
    user="song1",
    password="1q2w3e4r",
    db="yangsong2",
    charset="utf8",
)
cur = conn.cursor()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/yangsong2", methods=["POST", "GET"])
def ys2_data():
    if request.method == "POST":
        print(request.json)
        machine_id = request.json.get("id")
        co2 = request.json.get("co2")
        temperature = request.json.get("temperature")
        humidity = request.json.get("humidity")

        if machine_id is None or machine_id not in [1, 2]:
            return {"result": "fail", "hint": "id"}
        if co2 is None or not isinstance(co2, (int, float)):
            return {"result": "fail", "hint": "co2"}
        if temperature is None or not isinstance(temperature, (int, float)):
            return {"result": "fail", "hint": "temperature"}
        if humidity is None or not isinstance(humidity, (int, float)):
            return {"result": "fail", "hint": "humidity"}

        cur.execute(
            f"INSERT INTO yang{machine_id} (co2, temperature, humidity) VALUES ({co2}, {temperature}, {humidity})"
        )

        conn.commit()

        return {"result": "success"}

        # return jsonify(result="success")
    elif request.method == "GET":
        conn.commit()
        cur.execute("SELECT * FROM yang1")
        # cur.execute("SELECT * FROM yang1 WHERE DATE(stamp)=CURDATE()")
        rows = cur.fetchall()
        # idx stamp co2 temperature humidity
        labels = []
        co2s = []
        temperatures = []
        humidities = []
        for row in rows:
            if 404 in row or -404 in row:
                continue
            labels.append(row[1] - datetime.timedelta(hours=9))
            co2s.append(row[2])
            temperatures.append(row[3])
            humidities.append(row[4])

        return {
            "result": "success",
            "labels": labels,
            "co2s": co2s,
            "temperatures": temperatures,
            "humidities": humidities,
        }
    return abort(404)


if __name__ == "__main__":
    app.run("0.0.0.0", port=80, debug=True)