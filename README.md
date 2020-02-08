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
* Install spidev Python library
    * sudo apt-get install python3-spidev
* Enable the spi master
    * sudo raspi-config
    * 5 Interface Options
    * P5 SPI
