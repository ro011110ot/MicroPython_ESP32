# Import own Functions
import dht11
import oled
import wifi

# Imports
# from time import sleep    # activate when measure every 30 Min !

wifi.connect()
oled.oled_hello()
dht11.dht11()

# measure every 30 Min
# while True:
#   dht11.dht11()
#   sleep(1800)
