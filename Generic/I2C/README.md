# Inter-Integrated Circuit I2C/IIC

Inter-Integrated Circuit aka I2C or IIC -> https://en.wikipedia.org/wiki/I2C

Used as a serial communication bus, allowing you to chain multiple peripherals, and use addresses to read and write information from and to them. On microcontrollers I2C pins are usually indicated by SCL and SDA. The following code example scans the communications bus and prints out the address of the found components.

## Library

The Wire library (https://docs.arduino.cc/language-reference/en/functions/communication/wire/) is included in the Arduino framework.

## Code Example

```cpp
#include <Arduino.h>
#include <Wire.h>

void setup() {
  Wire.begin(5, 4); // SDA, SCL
  Serial.begin(115200);
  while(!Serial);
  Serial.println("\nI2C Scanner");
}

void loop() {
  uint8_t error, address;
  int nDevices;
  Serial.println("Scanning...");
  nDevices = 0;
  for(address = 1; address < 127; address++ ) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address<16) {
        Serial.print("0");
      }
      Serial.println(address,HEX);
      nDevices++;
    }
    else if (error==4) {
      Serial.print("Unknow error at address 0x");
      if (address<16) {
        Serial.print("0");
      }
      Serial.println(address,HEX);
    }
  }
  if (nDevices == 0) {
    Serial.println("No I2C devices found\n");
  }
  else {
    Serial.println("done\n");
  }
  delay(5000);
}
```
