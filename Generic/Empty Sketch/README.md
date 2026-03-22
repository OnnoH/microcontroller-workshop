# Empty Sketch

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
