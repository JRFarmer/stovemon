# stovemon
Wood stove temperature monitor using RPi, Adafruit IO and thermocouple amplifier

## Hardware

* Raspberry Pi (whichever version, including Pi Zero models)
* Adafruit Thermocouple Amplifier MAX31855 breakout board
* K-type thermocouple
* Adafruit 0.56" 4-Digit 7-Segment Display w/I2C Backpack

Connect the thermocouple to the thermocouple amplifier.
Connect the thermocouple amplifier to the Raspberry Pi.
Connect the 4-digit display to the Raspberry Pi.

## Configure Raspberry PI

* Install raspbian or raspbian lite. 
    * https://www.raspberrypi.org/documentation/installation/installing-images/
* Install spidev Python library
    * sudo apt-get install python3-spidev
* Enable the spi master
    * sudo raspi-config
    * 5 Interface Options
    * P5 SPI
* Install the Adafruit IO Python API: https://github.com/adafruit/Adafruit_IO_Python
    * Might need to do this:
        * sudo apt-get update
        * sudo apt-get install python3-pip
    * sudo pip3 install adafruit-io
* Install the Adafruit CircuitPython driver for MAX31855 Thermocouple Amplifier: https://github.com/adafruit/Adafruit_CircuitPython_MAX31855
    * sudo pip3 install adafruit-circuitpython-max31855
* Install the Adafruit 7-segment LED library: https://github.com/adafruit/Adafruit_CircuitPython_HT16K33
    * sudo pip3 install adafruit-circuitpython-ht16k33
* Install the systemd library
    *  sudo apt-get install python3-systemd
