#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# plug RX into TX on the RaspberryPi board (pins 8 and 10)
# https://www.raspberrypi.org/forums/viewtopic.php?t=153514#p1007843

from __future__ import print_function
import serial

test_string = "Testing 1 2 3 4".encode('utf-8')

port_list = ["/dev/serial0", "/dev/ttyS0"]

for port in port_list:
    try:
        serialPort = serial.Serial(port, 115200, timeout = 2)
        serialPort.flushOutput()
        serialPort.flushInput()  # Syntax may change in new version of python3-serial
        print("Opened port", port, "for testing:")
        bytes_sent = serialPort.write(test_string)
        print("Sent", bytes_sent, "bytes")
        loopback = serialPort.read(bytes_sent)
        if loopback == test_string:
            print("Received", len(loopback), "valid bytes, Serial port", port, "working \n")
        else:
            print("Received incorrect data", loopback, "over Serial port", port, "loopback\n")
        serialPort.close()
    except:
        print("Failed at", port, "\n")
