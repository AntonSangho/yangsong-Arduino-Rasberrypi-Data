#include <DHT.h>

#define DHTPIN 2     // DHT22 데이터 핀
#define DHTTYPE DHT22   
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // DHT22 센서에서 온습도 읽기
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // 오류 검사: NaN (not a number) 값을 반환하는 경우
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // 시리얼 포트를 통해 데이터 전송
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.println(" *C");

  delay(2000); // 2초 간격으로 데이터 읽기
}

