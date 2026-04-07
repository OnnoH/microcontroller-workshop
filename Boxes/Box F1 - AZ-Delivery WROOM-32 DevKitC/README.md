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
- 1x HC-SR501 PIR (Passive Infrared) Motion Sensor
- 1x TTP223B Touch Sensor
- 1x HC-SR04 Ultrasonic Sensor
- 1x LCD 2004A (20x4 display)
- some coloured Dupont cable F-F
- some coloured Dupont cable F-M
- some coloured Dupont cable M-M

## Quick Start
