# Logic Level Converter

![4 channel logic level converter](assets/logic-level-converter.jpg)

Sometimes you need 5V for a sensor and you only have 3.3V on your microcontroller, or vice versa. Then a LLC comes in handy, that can convert High Voltage (HV) to Low Voltage (LV), and vice versa.

## Circuit

![4 channel logic level circuit diagram](assets/logic-level-converter-circuit-diagram.jpg)

Connect the microcontroller's 3.3V pin to LV, the 5V to HV and the ground to both GND. Then draw either 5V from HVx or 3.3V from LVx, where x depends on the number of channels the PCB has.

https://learn.sparkfun.com/tutorials/bi-directional-logic-level-converter-hookup-guide/all

## Wiring Scheme

![4 channel logic level wiring scheme](assets/logic-level-converter-wiring-scheme.png)
