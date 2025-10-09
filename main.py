# Import own Functions
import dht11
import oled
import wifi

# Imports
from time import sleep  # activate when measure every 30 Min !

wifi.connect()
oled.start_timer()
dht11.dht11()

# measure every 15 Min
while True:
    dht11.dht11()
    sleep(900)
