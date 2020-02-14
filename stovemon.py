import sys
import time
import configparser

import MAX31855
import Adafruit_IO

import board
from adafruit_ht16k33 import segments

def main(cfgfile):

    # setup the display
    i2c = board.I2C()
    display = segments.Seg7x4(i2c)
    display.brightness = 3

    # while initializing, show something
    display.fill(0)
    display.print("----")

    config = configparser.ConfigParser()
    config.read(cfgfile)

    ADAFRUIT_IO_USERNAME    = config["io.adafruit.com"]["USERNAME"]
    ADAFRUIT_IO_KEY         = config["io.adafruit.com"]["KEY"]
    TEMPERATURE_FEED        = config["io.adafruit.com"]["TEMP_FEED"]
    COLDJUNCTION_FEED       = config["io.adafruit.com"]["CJ_FEED"]
    SPIDEV_BUS              = int(config["spidev"]["BUS"])
    SPIDEV_DEVICE           = int(config["spidev"]["DEVICE"])

    # connect to io.adafruit
    aio = Adafruit_IO.Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    # setup the thermocouple connection
    thermo = MAX31855.MAX31855(SPIDEV_BUS, SPIDEV_DEVICE)

    count = 0
    while (True):

        data = thermo.read()

        # update the display
        i_temp = round(data["temperature"])
        display.print("{0:4d}".format(i_temp))

        if (count % 10 == 0):
            # push temperature
            temp_feed = aio.feeds(TEMPERATURE_FEED)
            aio.send_data(temp_feed.key, data["temperature"])

            # push cold junction temperature
            cj_feed = aio.feeds(COLDJUNCTION_FEED)
            aio.send_data(cj_feed.key, data["cold_junction"])

        count = count + 1
        time.sleep(1)

if __name__ == "__main__":
    main(sys.argv[1])
