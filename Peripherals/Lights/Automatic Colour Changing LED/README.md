# Automatic Colour Changing LED

![Automatic Colour Changing LED](assets/automatic-colour-changing-led.jpg)

This looks like an ordinary white LED until you plug it in. You'll notice an automatic colour change. Sadly you can't change the colours or the speed in which they change. For that you'll need an RGB LED.

## Pinout

![Automatic Colour Changing LED pinout](assets/automatic-colour-changing-led-pinout.png)

## Wiring Scheme

![Automatic Colour Changing LED wiring scheme](assets/automatic-colour-changing-led-wiring-scheme.png)

The LED may also come as a SY-034 module already mounted with a resistor.

![Automatic Colour Changing LED module](assets/automatic-colour-changing-led-module.jpg)

![Automatic Colour Changing LED module pinout](assets/automatic-colour-changing-led-module-pinout.webp)

In this case the S pin on the module goes to the GPIO pin on the controller and the - pin should be connected to the ground.

## Example Code

```cpp
#include <Arduino.h>

int ledPin = 15;

void setup()
{
    Serial.begin(115200);
    pinMode(ledPin, OUTPUT);
}

void loop()
{
    digitalWrite(ledPin, HIGH);
    delay(10000);
    digitalWrite(ledPin, LOW);
    delay(5000);
}
```
