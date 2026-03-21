# Microcontroller Workshop

Having fun with microcontrollers like ESPs, Arduinos, Picos etc.

https://en.wikipedia.org/wiki/Microcontroller

## Development

Two common environments to develop applications for microcontrollers are:

- PlatformIO (https://platformio.org)
- Arduino IDE (https://www.arduino.cc/en/software/)

Although there are many IDE integrations for PlatformIO, Visual Studio Code is the most seen one, easily accessible via the extension manager.

The Arduino IDE targets the Arduino boards of course, but supports other flavours (like Expressiff as well)

Next to the UI differences, you might notice that PlatformIO uses `.cpp` as a file extension versus `.ino` on the Arduino IDE 😉

## Example Code

```cpp
#include <Arduino.h>

// put function declarations here:
int myFunction(int, int);

void setup()
{
    // put your setup code here, to run once:
    int result = myFunction(2, 3);
}

void loop()
{
    // put your main code here, to run repeatedly:
}

// put function definitions here:
int myFunction(int x, int y)
{
    return x + y;
}
```

## Glossary

A B C D E F [G](#G) H I J K [L](#L) M N O [P](#P) Q R S T U [V](#V]) W X Y Z

<a name="G"></a>

#### G

- GPIO - [General-Purpose Input/Output](https://en.wikipedia.org/wiki/General-purpose_input/output)

<a name="L"></a>

#### L

- LED - [Light Emitting Diode](https://en.wikipedia.org/wiki/Light-emitting_diode)
- LDR - [Light Dependent Resistor](https://en.wikipedia.org/wiki/Photoresistor)

<a name="P"></a>

#### P

- PCB - [Printed Circuit Board](https://en.wikipedia.org/wiki/Printed_circuit_board)

<a name="V"></a>

#### V

- VCC [Voltage at the Common Collector](https://en.wikipedia.org/wiki/IC_power-supply_pin)
- VIN [Voltage Input](https://en.wikipedia.org/wiki/Voltage_divider)
