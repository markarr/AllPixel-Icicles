import random 
import time 
import bibliopixel
from bibliopixel.drivers.serial_driver import *
from bibliopixel.led import *

driver = DriverSerial(num = 100, type = LEDTYPE.WS2812B)

strip = LEDStrip(driver)
strip.all_off()
strip.update()

strip.setRGB(3, 255,255,255)