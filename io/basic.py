#  Blink an LED with the LGPIO library
#  Uses lgpio library, compatible with kernel 5.11
#  Author: William 'jawn-smith' Wilson

import time
import lgpio
import logging
from logging.handlers import RotatingFileHandler

FAN = 19

# open the gpio chip and set the LED pin as output
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, FAN)

set_temp = 55
release_temp = 50

log_formatter = logging.Formatter('%(asctime)s %(message)s')

logFile = './log'

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=64*1024, 
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)

try:
    while True:
        
        tFile = open('/sys/class/thermal/thermal_zone0/temp')
        temp = float(tFile.read())
        tempC = temp/1000
        app_log.info(tempC)
        print(tempC)
        if tempC > set_temp :
            lgpio.gpio_write(h, FAN, 1)

        if tempC < release_temp :
            lgpio.gpio_write(h, FAN, 0)

        time.sleep(4)
        
except KeyboardInterrupt:
    lgpio.gpio_write(h, FAN, 0)
    lgpio.gpiochip_close(h)