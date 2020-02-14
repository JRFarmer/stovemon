import sys
import time
import configparser

import MAX31855
import Adafruit_IO

import board
from adafruit_ht16k33 import segments

def main(cfgfile):

    config = configparser.ConfigParser()
    config.read(cfgfile)

    ADAFRUIT_IO_USERNAME    = config["io.adafruit.com"]["USERNAME"]
    ADAFRUIT_IO_KEY         = config["io.adafruit.com"]["KEY"]
    TEMPERATURE_FEED        = config["io.adafruit.com"]["TEMP_FEED"]
    TEMPERATURE_PERIOD      = int(config["io.adafruit.com"]["TEMP_PERIOD"])
    COLDJUNCTION_FEED       = config["io.adafruit.com"]["CJ_FEED"]
    CJ_PERIOD               = int(config["io.adafruit.com"]["CJ_PERIOD"])

    SPIDEV_BUS              = int(config["spidev"]["BUS"])
    SPIDEV_DEVICE           = int(config["spidev"]["DEVICE"])

    DISPLAY_BRIGHTNESS      = int(config["display"]["BRIGHTNESS"])
    DISPLAY_PERIOD          = int(config["display"]["PERIOD"])

    # connect to io.adafruit
    aio = Adafruit_IO.Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    # setup the thermocouple connection
    thermo = MAX31855.MAX31855(SPIDEV_BUS, SPIDEV_DEVICE)

    # setup the display
    i2c = board.I2C()
    display = segments.Seg7x4(i2c)
    display.brightness = DISPLAY_BRIGHTNESS

    # while initializing, show something
    display.fill(0)
    display.print("----")

    count = 0
    while (True):

        data = thermo.read()

        if (count % DISPLAY_PERIOD == 0):
            # update the display
            i_temp = round(data["temperature"])
            display.print("{0:4d}".format(i_temp))

        if (count % TEMPERATURE_PERIOD == 0):
            # push temperature
            temp_feed = aio.feeds(TEMPERATURE_FEED)
            aio.send_data(temp_feed.key, data["temperature"])

        if (count % CJ_PERIOD == 0):
            # push cold junction temperature
            cj_feed = aio.feeds(COLDJUNCTION_FEED)
            aio.send_data(cj_feed.key, data["cold_junction"])

        count = count + 1
        time.sleep(1)

if __name__ == "__main__":
    main(sys.argv[1])
