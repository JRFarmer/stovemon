# stovemon
Wood stove temperature monitor using RPi, Adafruit IO and thermocouple amplifier

## Hardware

* Raspberry Pi (whichever version, including Pi Zero models)
* Adafruit Thermocouple Amplifier MAX31855 breakout board
* K-type thermocouple

Connect the thermocouple to the thermocouple amplifier.
Connect the thermocouple amplifier to the Raspberry Pi.

## Configure Raspberry PI

* Install raspbian or raspbian lite. 
    * https://www.raspberrypi.org/documentation/installation/installing-images/
* Install i2c-tools
    * sudo apt-get install i2c-tools
* Install i2c Python library
    * sudo apt-get install python3-smbus
* Enable the i2c master
    * sudo raspi-config
    * 5 Interface Options
    * P5 I2C
