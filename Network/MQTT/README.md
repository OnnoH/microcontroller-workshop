# MQTT

Sending messages over a network is the foundation of the Internet of Things (IoT). MQTT (Message Queuing Telemetry Transport) is a lightweight messaging protocol designed for efficient communication between devices, particularly in environments with limited bandwidth, such as IoT.

Because ESPs have the WiFi capability built-in, sending and receiving messages via MQTT only requires a client. The sketches below show a simple implementation. Next to the client, you'll need a server of course. This `docker-compose.yml` will spin up Mosquitto on your `localhost` which your client can talk to.

```
services:
  mosquitto:
    image: eclipse-mosquitto
    container_name: mosquitto
    volumes:
      - ./data/mosquitto/config:/mosquitto/config
      - ./data/mosquitto/data:/mosquitto/data
      - ./data/mosquitto/log:/mosquitto/log
    ports:
      - 1883:1883
      - 9001:9001
    stdin_open: true
    tty: true
```

Create the file in a suitable folder and then create the data folders

```shell
mkdir -p data/mosquitto/config && mkdir -p data/mosquitto/data && mkdir -p data/mosquitto/log
```

then start the server

```shell
docker compose up --detach
```

and start communicating.

To monitor the messages, [MQTT Explorer](https://mqtt-explorer.com) is quite a nice tool, but there are multiple solutions out there.

## ESP8266

```cpp
#include <ESP8266WiFi.h>
#include <MQTTClient.h>
#include <ArduinoJson.h>

const char WIFI_SSID[] = "YOUR_WIFI_SSID";     // CHANGE TO YOUR WIFI SSID
const char WIFI_PASSWORD[] = "YOUR_WIFI_PASSWORD";  // CHANGE TO YOUR WIFI PASSWORD

const char MQTT_BROKER_ADRRESS[] = "YOUR_BROKER_IP";  // CHANGE TO MQTT BROKER'S ADDRESS
const int MQTT_PORT = 1883;
const char MQTT_CLIENT_ID[] = "YOUR-FIRST_NAME";  // CHANGE IT AS YOU DESIRE
const char MQTT_USERNAME[] = "";                  // CHANGE IT BUT NOT REQUIRED, SO EMPTY IS FINE
const char MQTT_PASSWORD[] = "";                  // CHANGE IT BUT NOT REQUIRED, SO EMPTY IS FINE

// The MQTT topics that Arduino should publish/subscribe
const char PUBLISH_TOPIC[] = "sensor-readings/YOUR-FIRST_NAME";    // CHANGE IT AS YOU DESIRE
const char SUBSCRIBE_TOPIC[] = "sensor-readings/YOUR-FIRST_NAME";  // CHANGE IT AS YOU DESIRE

const int PUBLISH_INTERVAL = 5000;  // 5 seconds

WiFiClient network;
MQTTClient mqtt = MQTTClient(256);

unsigned long lastPublishTime = 0;

void setup() {
  Serial.begin(9600);

  int status = WL_IDLE_STATUS;
  while (status != WL_CONNECTED) {
    Serial.print("Arduino - Attempting to connect to SSID: ");
    Serial.println(WIFI_SSID);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    // wait 10 seconds for connection:
    delay(10000);
  }
  // print your board's IP address:
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  connectToMQTT();
}

void loop() {
  mqtt.loop();

  if (millis() - lastPublishTime > PUBLISH_INTERVAL) {
    sendToMQTT();
    lastPublishTime = millis();
  }
}

void connectToMQTT() {
  // Connect to the MQTT broker
  mqtt.begin(MQTT_BROKER_ADRRESS, MQTT_PORT, network);

  // Create a handler for incoming messages
  mqtt.onMessage(messageHandler);

  Serial.print("Arduino - Connecting to MQTT broker");

  while (!mqtt.connect(MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD)) {
    Serial.print(".");
    delay(100);
  }
  Serial.println();

  if (!mqtt.connected()) {
    Serial.println("Arduino - MQTT broker Timeout!");
    return;
  }

  // Subscribe to a topic, the incoming messages are processed by messageHandler() function
  if (mqtt.subscribe(SUBSCRIBE_TOPIC))
    Serial.print("Arduino - Subscribed to the topic: ");
  else
    Serial.print("Arduino - Failed to subscribe to the topic: ");

  Serial.println(SUBSCRIBE_TOPIC);
  Serial.println("Arduino - MQTT broker Connected!");
}

void sendToMQTT() {
  StaticJsonDocument<200> message;
  message["timestamp"] = millis();
  message["data"] = analogRead(0);  // Or you can read data from other sensors
  char messageBuffer[512];
  serializeJson(message, messageBuffer);

  mqtt.publish(PUBLISH_TOPIC, messageBuffer);

  Serial.println("Arduino - sent to MQTT:");
  Serial.print("- topic: ");
  Serial.println(PUBLISH_TOPIC);
  Serial.print("- payload:");
  Serial.println(messageBuffer);
}

void messageHandler(String &topic, String &payload) {
  Serial.println("Arduino - received from MQTT:");
  Serial.println("- topic: " + topic);
  Serial.println("- payload:");
  Serial.println(payload);
}
```

## ESP32

```cpp
#include <WiFi.h>
#include <MQTTClient.h>
#include <ArduinoJson.h>

const char WIFI_SSID[] = "YOUR_WIFI_SSID";     // CHANGE TO YOUR WIFI SSID
const char WIFI_PASSWORD[] = "YOUR_WIFI_PASSWORD";  // CHANGE TO YOUR WIFI PASSWORD

const char MQTT_BROKER_ADRRESS[] = "YOUR_BROKER_IP";  // CHANGE TO MQTT BROKER'S ADDRESS
const int MQTT_PORT = 1883;
const char MQTT_CLIENT_ID[] = "YOUR-FIRST_NAME";  // CHANGE IT AS YOU DESIRE
const char MQTT_USERNAME[] = "";                  // CHANGE IT BUT NOT REQUIRED, SO EMPTY IS FINE
const char MQTT_PASSWORD[] = "";                  // CHANGE IT BUT NOT REQUIRED, SO EMPTY IS FINE

// The MQTT topics that Arduino should publish/subscribe
const char PUBLISH_TOPIC[] = "sensor-readings/YOUR-FIRST_NAME";    // CHANGE IT AS YOU DESIRE
const char SUBSCRIBE_TOPIC[] = "sensor-readings/YOUR-FIRST_NAME";  // CHANGE IT AS YOU DESIRE

const int PUBLISH_INTERVAL = 5000;  // 5 seconds

WiFiClient network;
MQTTClient mqtt = MQTTClient(256);

unsigned long lastPublishTime = 0;

void setup() {
  Serial.begin(9600);

  int status = WL_IDLE_STATUS;
  while (status != WL_CONNECTED) {
    Serial.print("Arduino - Attempting to connect to SSID: ");
    Serial.println(WIFI_SSID);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    // wait 10 seconds for connection:
    delay(10000);
  }
  // print your board's IP address:
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  connectToMQTT();
}

void loop() {
  mqtt.loop();

  if (millis() - lastPublishTime > PUBLISH_INTERVAL) {
    sendToMQTT();
    lastPublishTime = millis();
  }
}

void connectToMQTT() {
  // Connect to the MQTT broker
  mqtt.begin(MQTT_BROKER_ADRRESS, MQTT_PORT, network);

  // Create a handler for incoming messages
  mqtt.onMessage(messageHandler);

  Serial.print("Arduino - Connecting to MQTT broker");

  while (!mqtt.connect(MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD)) {
    Serial.print(".");
    delay(100);
  }
  Serial.println();

  if (!mqtt.connected()) {
    Serial.println("Arduino - MQTT broker Timeout!");
    return;
  }

  // Subscribe to a topic, the incoming messages are processed by messageHandler() function
  if (mqtt.subscribe(SUBSCRIBE_TOPIC))
    Serial.print("Arduino - Subscribed to the topic: ");
  else
    Serial.print("Arduino - Failed to subscribe to the topic: ");

  Serial.println(SUBSCRIBE_TOPIC);
  Serial.println("Arduino - MQTT broker Connected!");
}

void sendToMQTT() {
  StaticJsonDocument<200> message;
  message["timestamp"] = millis();
  message["data"] = analogRead(0);  // Or you can read data from other sensors
  char messageBuffer[512];
  serializeJson(message, messageBuffer);

  mqtt.publish(PUBLISH_TOPIC, messageBuffer);

  Serial.println("Arduino - sent to MQTT:");
  Serial.print("- topic: ");
  Serial.println(PUBLISH_TOPIC);
  Serial.print("- payload:");
  Serial.println(messageBuffer);
}

void messageHandler(String &topic, String &payload) {
  Serial.println("Arduino - received from MQTT:");
  Serial.println("- topic: " + topic);
  Serial.println("- payload:");
  Serial.println(payload);
}
```
