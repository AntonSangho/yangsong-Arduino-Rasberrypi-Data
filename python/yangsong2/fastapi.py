from fastapi import FastAPI
from pydantic import BaseModel
import pymysql


class Ys2Data(BaseModel):
    id: int
    co2: float
    temperature: float
    humidity: float


app = FastAPI()

conn = pymysql.connect(
    host="127.0.0.1", user="song1", password="1q2w3e4r", db="yangsong2", charset="utf8"
)
cur = conn.cursor()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/yang1")
async def yang1(ys2_data: Ys2Data):
    if ys2_data.id not in [1, 2]:
        return {"result": "fail"}
    cur.execute(
        f"INSERT INTO yang{ys2_data.id} (co2, temperature, humidity) VALUES ({ys2_data.co2}, {ys2_data.temperature}, {ys2_data.humidity})"
    )
    # cur.execute(
    #     "INSERT INTO yang"
    #     + str(ys2_data.id)
    #     + " (co2, temperature, humidity) VALUES ("
    #     + str(ys2_data.co2)
    #     + ","
    #     + str(ys2_data.temperature)
    #     + ","
    #     + str(ys2_data.humidity)
    #     + ")"
    # )
    conn.commit()
    return {"result": "success", "data": ys2_data}
