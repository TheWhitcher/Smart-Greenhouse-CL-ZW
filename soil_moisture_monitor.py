# Name:     soil_moisture_monitor.py
# By:       Christophe Landry & Zacharyah Whitcher
# Date:     2023-11-24
# Version:  1.0

# Imports
import RPi.GPIO as GPIO
import time
import ADC0832_1

# Motor Pins
WATER_PUMP = 22

# Global Variables
pump_cooldown = False

# Setup the Components
def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(WATER_PUMP, GPIO.OUT)
	GPIO.output(WATER_PUMP, GPIO.LOW)
	ADC0832_1.setup()

# Clean up the GPIO
def destroy():
	GPIO.cleanup()
	
# Turn the water pump on or off
def handlePump(status=False):
	if (status): # stop
		GPIO.output(WATER_PUMP, GPIO.LOW)
	else:
		GPIO.output(WATER_PUMP, GPIO.HIGH)

# Read the sensor and return the results
def readSensor():
	res = ADC0832_1.getADC(0)
	moisture = ((255 - res) / 255) * 100
	moisture = round(moisture, 2)
	#print ('analog value: %03d  moisture: %d' %(res, moisture))
		
	return moisture
	
# Run the water pump
def RunPump():
	global pump_cooldown
	
	if(not pump_cooldown):
		pump_cooldown = True
		handlePump(True)
		time.sleep(3)
		handlePump(False)
		pump_cooldown = False

# Manual override to turn the water pump on and off.
def manualOverride(status=False):
	if(status):
		handlePump(True)
	else:
		handlePump(False)

# Main loop every 0.5 seconds
def loop():
	while True:
		readSensor()

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
