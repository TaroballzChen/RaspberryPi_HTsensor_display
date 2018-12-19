#!/usr/bin/python3
import sys
import Adafruit_DHT

while True:
    h,t = Adafruit_DHT.read_retry(11,4)
    print("%s C, %s %%"%(t,h))