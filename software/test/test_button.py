# -*- coding: utf-8 -*-
from gpiozero import Button

"""
Thanks to: 

printer resources:
https://github.com/adafruit/Adafruit_CircuitPython_Thermal_Printer/blob/master/examples/thermal_printer_simpletest.py
https://forums.adafruit.com/viewtopic.php?f=19&t=56504

button resources:
https://www.raspberrypi.org/documentation/usage/gpio/python/README.md
"""

CONFIG_FILENAME = 'config.json'

BUTTON_PIN = 23


if __name__ == '__main__':
    button = Button(BUTTON_PIN)

    while True:
        button.wait_for_press()
        print('***button pressed***')
        button.wait_for_release()
