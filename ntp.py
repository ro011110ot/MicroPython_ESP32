"""
This module provides a function to get the current time from an NTP server and adjust it to
Central European Time (CET/CEST) with daylight saving.
"""
import time


def cettime():
    """
    Calculates the current Central European Time (CET/CEST) including daylight saving.

    It determines if the current date is within the daylight saving period for Europe
    (last Sunday of March to last Sunday of October) and applies the corresponding
    UTC offset.

    Returns:
        tuple: A tuple formatted for `machine.RTC().datetime()`:
               (year, month, day, weekday, hour, minute, second, subsecond)
    """
    year = time.localtime()[0]
    dst_start = time.mktime(
        (year, 3, (31 - (int(5 * year / 4 + 4)) % 7), 1, 0, 0, 0, 0, 0)
    )
    dst_end = time.mktime(
        (year, 10, (31 - (int(5 * year / 4 + 1)) % 7), 1, 0, 0, 0, 0, 0)
    )
    now = time.time()
    if now < dst_start:
        cet_tuple = time.localtime(now + 3600)  # CET: UTC+1H
    elif now < dst_end:
        cet_tuple = time.localtime(now + 7200)  # CEST: UTC+2H
    else:
        cet_tuple = time.localtime(now + 3600)  # CET: UTC+1H

    # time.localtime() Format: (Y, M, D, h, m, s, wday_0-6, yday_1-366)

    # Adjust weekday for RTC (from 0-6 to 1-7, if necessary)
    # And: time.localtime()[6] (wday) is 0-6. rtc.datetime() expects it at index 3.
    # rtc.datetime() expects (Y, M, D, wday, h, m, s, subseconds)

    year, month, day, hour, minute, second, weekday_0_6, _ = cet_tuple

    # Assumption: rtc.datetime expects weekday (1-7) at index 3, and subseconds (0) at index 7.
    # If weekday_0_6 (e.g. 3 for Thursday) is correct, then:
    weekday_1_7 = weekday_0_6 + 1

    # Create the RTC tuple
    rtc_tuple = (year, month, day, weekday_1_7, hour, minute, second, 0)

    return rtc_tuple
