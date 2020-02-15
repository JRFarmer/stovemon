import sys
import time
import configparser

import board
import Adafruit_IO
from adafruit_ht16k33 import segments
from adafruit_max31855 import MAX31855

def ctof(cel):
    return cel * 180 / 100 + 32

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
    thermo = MAX31855(board.SPI(), SPIDEV_DEVICE)

    # setup the display
    i2c = board.I2C()
    display = segments.Seg7x4(i2c)
    display.brightness = DISPLAY_BRIGHTNESS

    # while initializing, show something
    display.fill(0)
    display.print("----")

    count = 0
    while (True):

        temp = ctof(thermo.temperature)

        if (count % DISPLAY_PERIOD == 0):
            # update the display
            i_temp = round(temp)
            display.print("{0:4d}".format(i_temp))

        if (count % TEMPERATURE_PERIOD == 0):
            # push temperature
            temp_feed = aio.feeds(TEMPERATURE_FEED)
            aio.send_data(temp_feed.key, temp)

        if (count % CJ_PERIOD == 0):
            ref = temp = ctof(thermo.reference_temperature)

            # push cold junction temperature
            cj_feed = aio.feeds(COLDJUNCTION_FEED)
            aio.send_data(cj_feed.key, ref)

        count = count + 1
        time.sleep(1)

if __name__ == "__main__":
    main(sys.argv[1])
