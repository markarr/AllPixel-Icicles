import random 
import time 
import bibliopixel
from bibliopixel.drivers.serial_driver import *
from bibliopixel.led import *

LED_Count = 300
driver = DriverSerial(num = LED_Count, type = LEDTYPE.WS2812B)
LED_Groups = 11  # Number of LED Groups

band = [[0 for x in xrange(5)] for x in xrange(24)] #Rand band
smice = [[0 for x in xrange(5)] for x in xrange(12)] #Small ice
lgice = [[0 for x in xrange(10)] for x in xrange(11)] #Large ice

#indices
i = 0
j = 0
l = 0
m = 0
n = 0

# Number of Groups
for x in range(LED_Groups):
	# First 5 in series go to random
	for j in xrange(5):
		band[l][j] = i
		i += 1
	l += 1
	# Next 5 are small ice
	for j in xrange(5):
		smice[m][j] = i
		i += 1
	# Next 5 are random
	for j in xrange(5):
		band[l][j] = i
		i += 1
	#next 10 are big ice
	for j in xrange(10):
		lgice[n][j] = i
		i += 1
	l += 1
	m += 1
	n += 1
	
# 5 more random
for j in xrange(5):
	band[l][j] = i
	i += 1
l += 1
# 5 more in small ice
for j in xrange(5):
	smice[m][j] = i
	i += 1
# 5 more random
for j in xrange(5):
	band[l][j] = i
	i += 1

# Function for Randoms
def bandRandom(strip, color, wait, iterations):
	for j in xrange(iterations):
		# 5 random pixels
		pixel = band[random.randint(0,23)][random.randint(0,4)]
		strip.set(pixel, color)
		# Show them
		strip.update()
		time.sleep(wait)
		strip.set(pixel, (0,0,0))
		# Turn them off
		strip.update()
		
# Function for Large Ice
def LargeIce(strip, color, wait, iterations):
	for j in xrange(iterations):
		# pick random ice
		strand = random.randint(0,9)
		# turn on the first one
		strip.set(lgice[strand][0], color)
		strip.update()
		time.sleep(wait)
		for x in xrange(9):
			# turn on the next one and the last one off
			strip.set(lgice[strand][x+1], color)
			strip.set(lgice[strand][x], (0,0,0))
			strip.update()
			time.sleep(wait)
		#turn the last pixel off
		strip.set(lgice[strand][x+1], (0,0,0))
		
# Function for Small Ice
def SmallIce(strip, wait, iterations):
	for j in xrange(iterations):
		# pick rand ice
		strand = random.randint(0,4)
		# turn on first one
		color = (0, 60, 200)
		strip.set(smice[strand][0], color)
		strip.update()
		time.sleep(wait)
		for x in xrange(3):
			# set the color
			if x == 0:
				color = (4, 68, 190)
			elif x == 1:
				color = (53, 120, 253)
			elif x == 2:
				color = (89, 135, 227)
			else:
				color = (127, 127, 127)
			# turn on the next one and off the last one
			strip.set(smice[strand][x+1], color)
			strip.set(smice[strand][x], (0,0,0))
			strip.update()
			time.sleep(wait)
		#turn off the last pixel
		strip.set(smice[strand][x+1], (0,0,0))
		
# Function for a color Wipe
def colorWipe(strip, color, wait_ms=50):
	#Wipe color across display a pixel at a time.
	for i in range(LED_Count):
		#turn light one
		strip.set(i, color)
		strip.update()
		time.sleep(wait_ms/1000.0)
		#turn light off
		strip.set(i, (0,0,0))
		strip.update()
		
# Initalize the NeoPixels
strip = LEDStrip(driver)
strip.all_off()
strip.update()

# First do a ColorWipe
colorWipe(strip, (127, 127, 127))


#begin the loop
print 'Press Ctrol-C to quit'
while True:
	a = threading.Thread(target=bandRandom, args=(strip, (127, 127, 127), 1, 10,))
	b = threading.Thread(target=SmallIce, args=(strip, 1, 2,))
	c = threading.Thread(target=LargeIce, args=(strip, (127, 127, 127), 1, 1,))
	if not a or not a.is_alive():
	    a.daemon = True
	    a.start()
	if not b or not b.is_alive():
	    b.daemon = True
	    b.start()
	if not c or not c.is_alive():
	    c.daemon = True
	    c.start()
	a.join()
	b.join()
	c.join()
	time.sleep(0.1)