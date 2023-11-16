#include <WiFiEsp.h> // Use this for WiFi instead of Ethernet.h
#include <ArduinoJson.h>
#include "DHT.h"

#define WIFIBAUD 115200

#ifndef HAVE_HWSERIAL1
#include "SoftwareSerial.h"
SoftwareSerial Serial1(3, 4); // RX, TX
#define WIFIBAUD 9600
#endif

#define DHTPIN 2
#define DHTTYPE DHT22

// Sample query
char INSERT_SQL[] = "INSERT INTO yangsong2.yang1 (CO2, temperature, humidity) VALUES (%f, %f, %f)";
char query[128];

// WiFi card example
char ssid[] = "tresc3-2.4G"; // your SSID
char pass[] = "tresc333";    // your SSID Password
char server[] = "192.168.0.18";

WiFiEspClient client; // Use this for WiFi instead of EthernetClient

DHT dht(DHTPIN, DHTTYPE);
float co2 = 0.0;
float humidity = 0.0;
float temperature = 0.0;

unsigned long dht_time;
unsigned long post_time;
unsigned long now_time;

void setup()
{
    Serial.begin(9600);
    while (!Serial)
        ; // wait for serial port to connect. Needed for Leonardo only
    dht.begin();
    // Begin WiFi section
    Serial1.begin(WIFIBAUD);
    WiFi.init(&Serial1);

    if (WiFi.status() == WL_NO_SHIELD)
    {
        Serial.println("WiFi shield not present");
        while (true)
            ;
    }

    Serial.print("\nConnecting to ");
    Serial.print(ssid);
    WiFi.begin(ssid, pass);
    while (WiFi.status() != WL_CONNECTED)
    {
        WiFi.begin(ssid, pass);
    }

    // print out info about the connection:
    Serial.println("\nConnected to network");
    Serial.print("My IP address is: ");
    Serial.println(WiFi.localIP());

    Serial.println("OK.");
}

void loop()
{
    now_time = millis();
    if (now_time - dht_time >= 2000)
    {
        co2 += 1.0;
        humidity = dht.readHumidity();
        temperature = dht.readTemperature();
        if (isnan(humidity) || isnan(temperature))
        {
            humidity = 404;
            temperature = 404;
        }
        dht_time = now_time;
    }
    if (now_time - post_time >= 5000 && client.connect(server, 80))
    {
        StaticJsonDocument<256> doc;
        doc["id"] = 1;
        doc["co2"] = co2;
        doc["temperature"] = temperature;
        doc["humidity"] = humidity;
        String jsondata = "";
        serializeJson(doc, jsondata);
        Serial.println(jsondata);

        client.println("POST /yangsong2 HTTP/1.1");
        client.println("Cache-Control: no-cache");
        client.print("Host: ");
        client.println(server);
        client.println("Content-Type: application/json");
        client.print("Content-Length: ");
        client.println(jsondata.length());
        client.println();
        client.println(jsondata);
        client.println();
        client.println();

        client.flush();
        client.stop();

        post_time = now_time;
    }
}
