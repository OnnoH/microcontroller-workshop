# Box D - NodeMCU

![NodeMCU](assets/nodemcu.jpg)

https://docs.cirkitdesigner.com/component/89e97846-8920-4a33-8e66-a4dbe70ee8b2

## Pinout

![NodeMCU pinout](assets/nodemcu-pinout.webp)

## Package Contents

- NodeMCU board
- 1x USB-A to MicroUSB cable
- 1x USA-A to USB-C adapter
- 1x 170 point breadboard (10 rows x 17 columns)
- 1x 10 kΩ resistor
- 3x 470 Ω resistors
- 5x LEDs (red, green, blue, yellow, white)
- 1x RGB LED
- 1x Colour Changing LED
- 1x Mini Push button
- 1x Piezo Buzzier
- 1x Water Sensor
- 1x DHT11 temperature and humidity sensor
- 1x AM312 PIR (Passive Infrared) motion sensor
- 1x TTP223B Touch Sensor
- 1x HC-SR04 Ultrasonic Sensor
- 1x SSD1306 OLED Display
- some coloured Dupont cable F-F
- some coloured Dupont cable F-M
- some coloured Dupont cable M-M

This board only has one 5V/VIN pin, so in order to connect all sensors, you'll need to create a power section on the breadboard.

## Quick Start

This board has a blue on-board LED that indicates upload activity. Also suitable for blinking every second

```cpp
#include <Arduino.h>

#define LED_PIN 2 // Onboard LED is on GPIO2

void setup() {
  pinMode(LED_PIN, OUTPUT); // Set LED pin as output
}

void loop() {
  digitalWrite(LED_PIN, LOW);  // Turn the LED on
  delay(1000);                 // Wait for 1 second
  digitalWrite(LED_PIN, HIGH); // Turn the LED off
  delay(1000);                 // Wait for 1 second
}
```
