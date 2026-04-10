# Arduino

Development with the help of the Arduino IDE:

- [Select](#Select) microcontroller
- [Write](#Write) code
- [Compile](#Compile) code
- [Deploy](#Deploy) to the microcontroller
- [Monitor](#Monitor) output

<a name="Select"></a>

## Select microcontroller

### Boards Manager

The Arduino IDE natively supports Arduino board, which is to be expected ;-)

In order to select the right ESP board, they first have to be installed. The [Boards Manager](https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-board-manager/) needs to know where to get that information.

First open up the preferences/settings dialog by pressing ⌘ , (Command comma, or Control comma on Windows)

![Arduino IDE preferences dialog](assets/boards-manager-configuration.png)

and put the following in the **Additional Boards manager URLs** field

```
https://dl.espressif.com/dl/package_esp32_index.json
https://arduino.esp8266.com/stable/package_esp8266com_index.json
```

Then head over to the boards manager itself, filter on _esp_ and click the 'Install' button.

![Arduino IDE boards manager](assets/boards-manager.png)

This will not only add the ESP boards to the list, but also installs the tool chain needed.

Note that on MacOS you may need to install the [Xcode Command Line Tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools)

```shell
xcode-select --install
```

### Drivers

On MacOS, connecting to a microcontroller either directly via USB or via an FTDI USB to Serial converter, will probably work out of the box. For Windows some drivers might be required. Some download links:

- [CH340](https://sparks.gogo.co.nz/ch340.html)
- [CP210x](https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads)

> TODO?? Explain UART and FDTI

<a name="Write"></a>

## Write code

This piece of code below continuously adds the number 2 and 3, but that's it. No input, no output.

What it does do, is demonstrate the structure of a microcontroller sketch.

```cpp
/*
    This is a not so useful sketch
*/
#include <Arduino.h>

#define NUMBER_ONE 2

const int numberTwo = 3;

int result;

// put function declarations here:
int myFunction(int, int);

void setup()
{
    // put your setup code here, to run once:
    int result = myFunction(NUMBER_ONE, numberTwo);
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

Comments are either preceeded by `//` or wrapped inside `/* ... */` and can clarify what's going on in the code.

`#include` pulls in constants and function definitions from libraries that are needed. In this case the 'core' Arduino library.

After that `define` global constants and variables. Constants cannot be changed during program execution, regular variable can.

Then put the so-called **forward declaration** of your functions. This is good practice, but not neccessary. The compiler looks at the sketch as a whole and figures out what goes where.

Just remember: A function can be

- declared
- defined
- called (or invoked)

In this case `myFunction()` is **declared** on top, **defined** at the botton and **called** from `setup()` in the middle.

Two special _reserved_ functions need to exist in an Arduino sketch: `setup()` and `loop()`. The first one is executed once and typically used to initialise the runtime enviroment. The second one is executed repeatedly and never stops (unless the power is unplugged).

See also: https://docs.arduino.cc/learn/programming/sketches/

<a name="Compile"></a>

## Compile code

<a name="Deploy"></a>

## Deploy to microcontroller

<a name="Monitor"></a>

## Monitor output
