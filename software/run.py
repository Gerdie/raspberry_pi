# -*- coding: utf-8 -*-
import json
import textwrap

import adafruit_thermal_printer
import board
import busio
from gpiozero import LED, Button

"""
Thanks to: 

printer resources:
https://github.com/adafruit/Adafruit_CircuitPython_Thermal_Printer/blob/master/examples/thermal_printer_simpletest.py
https://forums.adafruit.com/viewtopic.php?f=19&t=56504

button resources:
https://www.raspberrypi.org/documentation/usage/gpio/python/README.md
"""

STATE_FILENAME = 'state.json'
TEXT_FILENAME = 'ThomasOrdesLees_journal.txt'

BUTTON_PIN = 23
TX = board.TX
RX = board.RX


def format_text(text, maxColumn=32):
    # wrap text
    printer_text = textwrap.wrap(text, width=maxColumn)
    # add line breaks
    printer_text = [line + '\n' for line in printer_text]
    # reverse (for upside down printing)
    printer_text = printer_text[::-1]
    return ''.join(printer_text)


def get_next_line():
    with open(STATE_FILENAME, 'rw') as statefile:
        current_line = json.load('')
        last_line = ''
        # TODO: update current_line in file
        if current_line >= last_line:
            return '\n'
    with open(STATE_FILENAME, 'rw') as textfile:
        lines = textfile.readlines()
        return lines[current_line]


def get_printer():
    # TODO: print a test page & verify printer class & bandrate
    ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
    uart = busio.UART(TX, RX, baudrate=19200)

    printer = ThermalPrinter(uart, auto_warm_up=False)
    printer.warm_up()

    printer.upside_down = True
    printer.size = adafruit_thermal_printer.SIZE_SMALL
    printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT

    return printer


def button_callback(_channel):
    printer = get_printer()
    next_line = get_next_line()
    formatted_line = format_text(next_line)
    printer.print(formatted_line)


if __name__ == '__main__':
    button = Button(BUTTON_PIN)
    printer = get_printer()

    while True:
        button.wait_for_press()
        next_line = get_next_line()
        formatted_line = format_text(next_line)
        printer.print(formatted_line)
        button.wait_for_release()
