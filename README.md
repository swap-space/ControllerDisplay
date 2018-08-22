# ControllerDisplay
Uses PySerial and PyGame to display controller inputs which are submitted over a serial terminal

Values are expected to be submitted to the port pecified in the config.json file as the string representation of a number in base 10. This number is treated as a bit field with bits representing button states. The least significant bit in the value received represents the first button defined in JSON and so on.

For example, if the 'A' button is pressed on a controller, and 'A' is the 3rd button defined in JSON, then the third bit of the submitted bit field should be set, i.e. 0000 0100. This is a value of 0x04, and so the string submitted over the specified serial port should be "4". If, however, 'A' was the 6th button defined in JSON then the value would be 0010 0000, or 0x20, or as a decimal string to be submitted over serial "64".

A sample configuration is given to make use of a SNES controller. An arduino source file will be uploaded shortly to complement this.

The included SNES controller image is from https://commons.wikimedia.org/wiki/File:SNES_controller.svg