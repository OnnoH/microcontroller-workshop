# Box B - AZ-Delivery Envy

![AZ-Envy](assets/az-envy.jpg)
[AZ-Envy - the somewhat different Micro Controller Board](https://www.az-delivery.de/blogs/az-delivery-blog-en/az-envy-the-somewhat-different-micro-controller-board)

[Article]https://www.az-delivery.de/en/products/az-envy
[Data Sheet](assets/doc/AZ-Envy_Datasheet.pdf)
[Manual](assets/doc/Manual_AZ-Envy_Ver.1.0_EN.pdf)
[Pinout](assets/doc/AZ-Envy_Pinout.pdf)
[3D Print Case](assets/doc/3D_print.zip)

> The board does not have an UART so programming requires hooking up a USB to TTL adapter.

## Pinout

![AZ-Delivery Envy pinout](assets/az-envy-pinout.png)

> The GPIO points are exposed by wires that are soldered on. Make sure to check the connection. // TODO

> Only the 3V3 is provided, so you'll need to connect a Logic Level Converter in order to get 5V.

## Package Contents

- 1x AZ-Delivery Envy board (with MQ2 and SHT30)
- 1x USB to TTL adapter
- 1x USB-A to MicroUSB cable
- 2x USA-A to USB-C adapter
- 1x [170 pins mini breadboard](../../Generic/Breadboard/README.md)
- 1x [mini push button](../../Peripherals/Switches/Button/README.md)
- 1x [Piezo Buzzer](../../Peripherals/Sound/Buzzer/README.md)
- 1x 10 kΩ resistor
- 3x 470 Ω resistor (red, red, brown, gold)
- 1x [Light Dependent Resistor (LDR)](../../Peripherals/Sensors/LDR%20Light%20Dependent%20Resistor/README.md)
- 1x [RGB LED](../../Peripherals/Lights/RGB%20LED/README.md)
- 5x [LEDs (red, green, blue, yellow, white)](../../Peripherals/Lights/Single%20Led/README.md)
- 1x [Logic Level Converter](../../Generic/Logic%20Level%20Converter/README.md)
- 1x [Colour Changing LED](../../Peripherals/Lights/Automatic%20Colour%20Changing%20LED/README.md)
- 1x [Water Sensor](../../Peripherals/Sensors/Water%20Sensor/README.md)
- 1x [DHT11 temperature and humidity sensor](../../Peripherals/Sensors/DHT11%20Temperature%20and%20Humidity%20Sensor/README.md)
- 1x [HC-SR501 PIR (Passive Infrared) Motion Sensor](../../Peripherals/Sensors/HC-SR501%20PIR%20Motion%20Sensor/README.md)
- 1x [TTP223B Touch Sensor](../../Peripherals/Sensors/TTP223B%20Touch%20Sensor/README.md)
- 1x [HC-SR04 Ultrasonic Sensor](../../Peripherals/Sensors/HC-SR04%20Ultrasonic%20Sensor/README.md)
- 1x [SSD1306 OLED Display](../../Peripherals/Displays/SSD1306%20OLED%20Display/README.md)
- some [Dupont Jumper cables](../../Generic/Wiring/README.md)

## Libraries

## Example Code

## Project

https://github.com/thorsten-l/ESP8266-AZ-Envy
