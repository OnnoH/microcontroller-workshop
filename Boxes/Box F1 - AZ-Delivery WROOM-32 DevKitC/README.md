# Box F1 - AZ-Delivery WROOM-32 DevKitC

This board comes in either `v2`
https://docs.cirkitdesigner.com/component/b3b995da-b93f-413a-bfa3-243d11a45844/esp32-dev-kit-c-v2-38-pins

or `v4`

https://docs.cirkitdesigner.com/component/de1ff842-ae52-41f8-9dbc-7e513b5bfd95

The main difference is that DevKitC `v4` uses the newer (but pin compatible) CP2102N USB to serial chip, which supports a higher maximum baud rate. The `v2` has CP2102.

The higher value of C9 at the EN pin may help the automatic reset circuit more reliably reset to the bootloader for flashing under some host configurations, particularly on Windows. However, it did not result in any common reports of this problem on `v2` with the smaller capacitor value.

All the other changes are cost/BoM optimisation rather than any functional fixes or improvements.

## Pinout

## Package Contents

- AZ-Delivery WROOM-32 DevKitC v2 board
- 1x USB-A to MicroUSB cable
- 1x USA-A to USB-C adapter
- 1x [170 pins mini breadboard](../../Generic/Breadboard/README.md)
- 1x [mini push button](../../Peripherals/Switches/Button/README.md)
- 1x [Piezo Buzzer](../../Peripherals/Sound/Buzzer/README.md)
- 1x 10 kΩ resistor
- 3x 470 Ω resistor (red, red, brown, gold)
- 1x [Light Dependent Resistor (LDR)](../../Peripherals/Sensors/LDR%20Light%20Dependent%20Resistor/README.md)
- 1x [RGB LED](../../Peripherals/Lights/RGB%20LED/README.md)
- 5x [LEDs (red, green, blue, yellow, white)](../../Peripherals/Lights/Single%20Led/README.md)
- 1x [Colour Changing LED](../../Peripherals/Lights/Automatic%20Colour%20Changing%20LED/README.md)
- 1x [Water Sensor](../../Peripherals/Sensors/Water%20Sensor/README.md)
- 1x [DHT11 temperature and humidity sensor](../../Peripherals/Sensors/DHT11%20Temperature%20and%20Humidity%20Sensor/README.md)
- 1x [TTP223B Touch Sensor](../../Peripherals/Sensors/TTP223B%20Touch%20Sensor/README.md)
- 1x [HC-SR04 Ultrasonic Sensor](../../Peripherals/Sensors/HC-SR04%20Ultrasonic%20Sensor/README.md)
- 1x [SSD1306 OLED Display](../../Peripherals/Displays/SSD1306%20OLED%20Display/README.md)
- 1x [HC-SR501 PIR (Passive Infrared) Motion Sensor](../../Peripherals/Sensors/HC-SR501%20PIR%20Motion%20Sensor/README.md)
- 1x [LCD 2004A (20x4 display)](../../Peripherals/Displays/LCD/README.md)
- some [Dupont Jumper cables](../../Generic/Wiring/README.md)

## Quick Start
