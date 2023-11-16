#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
	Serial.begin(9600);
	Serial.println("DHT22 test!");

	dht.begin();
}

void loop() {

	float h = dht.readHumidity();
	float t = dht.readTemperature();

	Serial.println(F("Humidity (%): "));
	Serial.print(h);

	Serial.println(F("Temperature (C): "));
	Serial.print(t);

	delay(2000);
}
