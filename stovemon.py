import sys
import time
import configparser

import MAX31855
import Adafruit_IO

def main(cfgfile):

    config = configparser.ConfigParser()
    config.read(cfgfile)p0

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

    while (True):

        data = thermo.read()

        # push temperature
        temp_feed = aio.feeds(TEMPERATURE_FEED)
        aio.send_data(temp_feed.key, data["temperature"])

        # push cold junction temperature
        cj_feed = aio.feeds(COLDJUNCTION_FEED)
        aio.send_data(cj_feed.key, data["cold_junction"])

        print(data)
        time.sleep(10)

if __name__ == "__main__":
    main(sys.argv[1])
