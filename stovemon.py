#!/usr/bin/python3

# standard python libraries
import sys
import time
import configparser
import systemd.daemon

# adafruit libraries
import board
from Adafruit_IO import Client
from adafruit_ht16k33 import segments
from adafruit_max31855 import MAX31855

def ctof(cel):
    return cel * 180 / 100 + 32

def read_retries(thermo, retries):

    try:
        temp = ctof(thermo.temperature)
        ref  = ctof(thermo.reference_temperature)
    except RuntimeError as e:
        if retries > 0:
            time.sleep(1)
            return read_retries(thermo, retries - 1)
        else:
            raise

    return temp, ref

def main(cfgfile):

    config = configparser.ConfigParser()
    config.read(cfgfile)

    TEMPERATURE_PERIOD      = int(config["io.adafruit.com"]["TEMP_PERIOD"])
    CJ_PERIOD               = int(config["io.adafruit.com"]["CJ_PERIOD"])
    DISPLAY_PERIOD          = int(config["display"]["PERIOD"])

    # setup the display
    i2c = board.I2C()
    display = segments.Seg7x4(i2c)
    display.brightness = int(config["display"]["BRIGHTNESS"])

    # while initializing, show something
    display.fill(0)
    display.print("----")

    # connect to io.adafruit
    aio = Client(config["io.adafruit.com"]["USERNAME"], 
                 config["io.adafruit.com"]["KEY"])
    temp_feed = aio.feeds(config["io.adafruit.com"]["TEMP_FEED"])
    cj_feed   = aio.feeds(config["io.adafruit.com"]["CJ_FEED"])

    # setup the thermocouple connection
    spi = board.SPI()
    thermo = MAX31855(spi, int(config["spidev"]["DEVICE"]))

    systemd.daemon.notify('READY=1')

    count = -1
    while (True):

        try:
            temp, ref = read_retries(thermo, 3)
        except RuntimeError as e:
            if "not connected" in str(e):
                display.print("-OC-") # open circuit
            elif "short" in str(e) and "ground" in str(e):
                display.print("SH-E") # short to earth
            elif "short" in str(e) and "power" in str(e):
                display.print("SH-P") # short to power
            raise

        if (count % DISPLAY_PERIOD == 0):
            # update the display
            i_temp = round(temp)
            display.print("{0:4d}".format(i_temp))

        if (count % TEMPERATURE_PERIOD == 0):
            # push temperature
            aio.send_data(temp_feed.key, temp)

        if (count % CJ_PERIOD == 0):
            # push cold junction temperature
            aio.send_data(cj_feed.key, ref)

        count = count + 1
        time.sleep(1)

if __name__ == "__main__":
    main(sys.argv[1])
