import time
import machine
import ntptime

def cettime():
    year = time.localtime()[0]
    HHMarch = time.mktime((year, 3, (31 - (int(5 * year / 4 + 4)) % 7), 1, 0, 0, 0, 0, 0))
    HHOctober = time.mktime((year, 10, (31 - (int(5 * year / 4 + 1)) % 7), 1, 0, 0, 0, 0, 0))
    now = time.time()
    if now < HHMarch:
        cet_tuple = time.localtime(now + 3600)  # CET: UTC+1H
    elif now < HHOctober:
        cet_tuple = time.localtime(now + 7200)  # CEST: UTC+2H
    else:
        cet_tuple = time.localtime(now + 3600)  # CET: UTC+1H

    # time.localtime() Format: (Y, M, D, h, m, s, wday_0-6, yday_1-366)

    # Wochentag für RTC anpassen (von 0-6 auf 1-7, falls nötig)
    # Und: time.localtime()[6] (wday) ist 0-6. rtc.datetime() erwartet ihn an Index 3.
    # rtc.datetime() erwartet (Y, M, D, wday, h, m, s, subseconds)

    jahr, monat, tag, stunde, minute, sekunde, wochentag_0_6, _ = cet_tuple

    # Annahme: rtc.datetime erwartet Wochentag (1-7) an Index 3, und subsekunden (0) an Index 7.
    # Wenn wochentag_0_6 (z.B. 3 für Donnerstag) richtig ist, dann:
    wochentag_1_7 = wochentag_0_6 + 1

    # Erstelle das RTC-Tupel
    rtc_tuple = (jahr, monat, tag, wochentag_1_7, stunde, minute, sekunde, 0)

    return rtc_tuple
