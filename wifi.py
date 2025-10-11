"""
This module handles the Wi-Fi connection for the ESP32.
"""

import machine
import network
import ntp
import ntptime
import time
from secrets import secrets

# WLAN configuration
wlan = network.WLAN(network.WLAN.IF_STA)


def check_wifi():
    """Checks Wi-Fi connection, reconnects if necessary."""
    if wlan.isconnected():
        return True
    else:
        return connect()


def connect():
    """
    Connects to the Wi-Fi network using credentials from the secrets file.

    If not connected, it will try to connect. If successful, it prints the
    network configuration and sets the real-time clock (RTC) from an NTP server.
    If it fails, it prints an error message.
    Returns True on success, False on failure.
    """
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(secrets["ssid"], secrets["password"])
        # Wait for connection with a timeout
        max_wait = 10
        while max_wait > 0:
            if wlan.isconnected():
                break
            max_wait -= 1
            time.sleep(3)

    if wlan.isconnected():
        print("network config:", wlan.ifconfig())
        ntptime.settime()
        rtc = machine.RTC()
        rtc.datetime(ntp.cettime())
        print("RTC set to:", time.localtime())
        return True
    else:
        print("Network is offline")
        return False
