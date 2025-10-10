# Import own Functions
import dht11
import oled
import wifi
import time

time_now = time.localtime()
min_now = time_now[4]
# Imports
from time import sleep, localtime  # activate when measure every 30 Min !

wifi.connect()
oled.start_timer()

# measure every 15 Min
if min_now == 00 or min_now == 15 or min_now == 30 or min_now == 45:
    dht11.dht11()
