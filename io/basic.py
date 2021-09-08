#  Blink an LED with the LGPIO library
#  Uses lgpio library, compatible with kernel 5.11
#  Author: William 'jawn-smith' Wilson

import time
import lgpio

FAN = 19

# open the gpio chip and set the LED pin as output
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, FAN)

set_temp = 55

release_temp = 50

try:
    while True:
        
        tFile = open('/sys/class/thermal/thermal_zone0/temp')
        temp = float(tFile.read())
        tempC = temp/1000
        print(tempC)
        if tempC > set_temp :
            lgpio.gpio_write(h, FAN, 1)

        if tempC < release_temp :
            lgpio.gpio_write(h, FAN, 0)

        time.sleep(4)
        
except KeyboardInterrupt:
    lgpio.gpio_write(h, FAN, 0)
    lgpio.gpiochip_close(h)