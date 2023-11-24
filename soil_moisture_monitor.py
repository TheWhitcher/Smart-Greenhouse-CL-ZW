# Name:     soil_moisture_monitor.py
# By:       Christophe Landry & Zacharyah Whitcher
# Date:     2023-11-24
# Version:  1.0

# Imports
import RPi.GPIO as GPIO
import time
import ADC0832_1

# Motor Pins
MotorPin_A = 5
MotorPin_B = 6

# Global Variables
global motor_cooldown
motor_cooldown = False

# Setup the Components
def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(MotorPin_A, GPIO.OUT)
	GPIO.setup(MotorPin_B, GPIO.OUT)
	motorStop()

# Clean up the GPIO and stop the motor
def destroy():
	#motorStop() #Not needed
	GPIO.cleanup()

# Stop the motor
def motorStop():
	GPIO.output(MotorPin_A, GPIO.HIGH)
	GPIO.output(MotorPin_B, GPIO.HIGH)
	
# Turn motor on and off
def motor(status, direction):
	if status == 0: # stop
		motorStop()
	else:
		if direction == 1:
			GPIO.output(MotorPin_A, GPIO.HIGH)
			GPIO.output(MotorPin_B, GPIO.LOW)
		else:
			GPIO.output(MotorPin_A, GPIO.LOW)
			GPIO.output(MotorPin_B, GPIO.HIGH)

# Read the sensor and return the results
def readSensor(max_moisture=100, min_moisture=50):
	res = ADC0832_1.getADC(0)
	moisture = ((255 - res) / 255) * 100
	moisture = round(moisture, 2)
	#print ('analog value: %03d  moisture: %d' %(res, moisture))
		
	return moisture
	
# Run the Water Motor
def RunMotor():
	global motor_cooldown
	
	if(motor_cooldown != True):
		motor_cooldown = True
		motor(1,0)
		time.sleep(10)
		motor(0,0)
		motor_cooldown = False
		
# Main loop every 0.5 seconds
def loop():
	while True:
		readSensor(150)

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
