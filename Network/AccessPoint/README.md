# Access Point

ESP boards have WiFi and Bluetooth connectivity built-in.

Setting up an access point is quite easy.

If you look at the example code you'll notice that there's only a difference in the `#include`.

## ESP8266

```cpp

#include <Arduino.h>
#include <ESP8266WiFi.h.h>

const char *ssid = "YOUR_SSID";
const char *password = "YOUR_PASSWORD";

void setup()
{
  Serial.begin(115200);
  Serial.println();
  delay(10);

  // Connect to Wi-Fi network with SSID and password
  Serial.println("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the AP (Access Point) to be open
  WiFi.softAP(ssid, password);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);
}

void loop()
{
  // No need to do anything here
}
```

## ESP32

```cpp
// Load Wi-Fi library
#include <WiFi.h>

// Replace with your network credentials
const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi network with SSID and password
  Serial.print("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the AP (Access Point) to be open
  WiFi.softAP(ssid, password);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  server.begin();
}

void loop(){
    // No need to do anything here.
}
```
