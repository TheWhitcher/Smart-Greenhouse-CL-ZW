# Name:     uv_light_monitor.py
# By:       Christophe Landry & Zacharyah Whitcher
# Date:     2023-11-24
# Version:  1.0

# Imports
import RPi.GPIO as GPIO
import time
import ADC0832_1

# UV Light
LED = 27

# Setup the Components
def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED, GPIO.OUT)
	GPIO.output(LED, GPIO.LOW)
	ADC0832_1.setup()

# Clean up the GPIO
def destroy():
	GPIO.cleanup()

# Read the sensor and return the results
def readSensor(max_uv=100, min_uv=50):
	res = ADC0832_1.getADC(1)
	if res < 0:
		res = 0
	if res > 100:
		res = 100
	#print ('res = %d' % res)

	if (res <= (max_uv + min_uv) / 2):
		GPIO.output(LED, GPIO.HIGH)
	elif (res > (max_uv + min_uv) / 2 ):
		GPIO.output(LED, GPIO.LOW)

# Main loop every 0.5 seconds
def loop():
	while True:
		readSensor(50)

# Main Program
if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt: 
		destroy()
		print ('The end !')
	finally:
		destroy()
