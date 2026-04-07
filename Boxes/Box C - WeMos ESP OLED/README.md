# Box C - WeMos ESP WROOM 32 OLED

![WeMos ESP32 Board with OLED](assets/wemos-esp-wroom-32-oled.jpg)

https://docs.cirkitdesigner.com/component/7786fc6a-a0ee-4b72-8fc5-21d56f61b3be
https://wiki.geekworm.com/WEMOS_ESP32_Board_with_OLED

## Pinout

![WeMos ESP32 Board with OLED pinout](assets/wemos-esp-wroom-32-oled-pinout.jpg)

## Package Contents

- 1x WeMos ESP 32 development board (with SSD1306 OLED Display)
- 1x USB-A to MicroUSB cable
- 1x USA-A to USB-C adapter
- 1x 170 point breadboard (10 rows x 17 columns)
- 1x 10 kΩ resistor (brown, black, orange, gold)
- 3x 470 Ω resistor
- 5x LEDs
- 1x RGB LED
- 1x Colour Changing LED
- 1x Mini Push button
- 1x Piezo Buzzer
- 1x Water Sensor
- 1x HC-SR04 Ultrasonic Sensor
- 1x DHT11 temperature and humidity sensor
- 1x AM312 PIR (Passive Infrared) motion sensor
- 1x TTP223B Touch Sensor
- some coloured Dupont cable F-F
- some coloured Dupont cable F-M
- some coloured Dupont cable M-M

## Quick Start

This board has an on-board OLED screen. The following sketch displays a simple text, but of course the possibilities are (almost) endless.

```cpp
#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  Serial.begin(115200);

  // Start I2C Communication SDA = 5 and SCL = 4 on Wemos Lolin32 ESP32 with built-in SSD1306 OLED
  Wire.begin(5, 4);

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C, false, false)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  delay(2000); // Pause for 2 seconds

  // Clear the buffer.
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.print(F("Hello, World!"));
  display.display();
}

void loop() {

}
```
