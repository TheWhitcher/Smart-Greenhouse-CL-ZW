# Name:     temperature_monitor.py
# By:       Christophe Landry & Zacharyah Whitcher
# Date:     2023-11-24
# Version:  1.0

# Imports
import os
import RPi.GPIO as GPIO
import ADC0832_2
import time
import math

# LED Pins
LED = 4 # Tested with a LED because no availabl fan

# Motor Pins
FAN_PIN_A = 19
FAN_PIN_B = 26

# Global Variables
fan_cooldown = False

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(LED, GPIO.OUT)
  GPIO.output(LED, GPIO.LOW)
  #GPIO.output(FAN_PIN_A, GPIO.OUT)
  #GPIO.output(FAN_PIN_B, GPIO.OUT)
  #fan_stop()
  ADC0832_2.setup()

# Stop the fan
def fan_stop():
	GPIO.output(FAN_PIN_A, GPIO.HIGH)
	GPIO.output(FAN_PIN_B, GPIO.HIGH)

# Turn fan on and off
def handleFan(status=0, direction=1):
	if status == 0: # stop
		print("Fan Stop")
		fan_stop()
	else:
		if direction == 1:
			print("Fan On")
			GPIO.output(FAN_PIN_A, GPIO.HIGH)
			GPIO.output(FAN_PIN_B, GPIO.LOW)
		else:
			GPIO.output(FAN_PIN_A, GPIO.LOW)
			GPIO.output(FAN_PIN_B, GPIO.HIGH)

# Run the fan.
def RunFan():
	global fan_cooldown
  
	if(not fan_cooldown):
		fan_cooldown = True
		handleFan(True)
		time.sleep(30)
		handleFan(False)
		fan_cooldown = False
		
# Get the temperature value in Celsius.
def readSensor():
  T25 = 25 + 273.15 #Convert to Kelvin
  R25 = 10000 #Resistance for degrees in Celcius
  B = 3455
  
  res = ADC0832_2.getADC(0)
  Vr = 3.3 * float(res) / 255
  #Rt = 10000 * Vr / (3.3 - Vr) //Our sensor is built different
  if (Vr != 0):
    Rt = (3.3 * 10000) / Vr - 10000
    #print ('Rt : %.2f' %Rt)
    if (Rt == 0):
       Rt = 0.1
    ln = math.log(Rt/R25)
    Tk = 1 / ((ln / B) + (1/T25))
    Tc = Tk - 273.15 # Convert to Celcius
    
    Tc = round(Tc, 2)
    return Tc

# Manual override to turn the HVAC on and off.
def manualOverride(status=False):
	if(status):
		handleLed(True)
		#handleFan(1)
	elif (not fan_cooldown):
		handleLed(False)
		#handleFan(0)

# Run the LED *Note: Used for testing
def RunLed():
	global fan_cooldown
  
	if(not fan_cooldown):
		fan_cooldown = True
		handleLed(True)
		time.sleep(30)
		handleLed(False)
		fan_cooldown = False
		
# Turn the Led on or off *Note: Used for testing
def handleLed(status=False):
	if (status): # stop
		#print("LED fan ON")
		GPIO.output(LED, GPIO.HIGH)
	else:
		#print("LED fan OFF")
		GPIO.output(LED, GPIO.LOW)
		
def loop():
  T25 = 25 + 273.15 #Convert to Kelvin
  R25 = 10000 #Resistance for degrees in Celcius
  B = 3455

  while True:
    res = ADC0832_2.getADC(0)
    Vr = 3.3 * float(res) / 255
    #Rt = 10000 * Vr / (3.3 - Vr) //Our sensor is built different
    if (Vr != 0):
      Rt = (3.3 * 10000) / Vr - 10000
      #print ('Rt : %.2f' %Rt)
      ln = math.log(Rt/R25)
      Tk = 1 / ((ln / B) + (1/T25))
      Tc = Tk - 273.15 # Convert to Celcius
      print('Tc : %.2f' %Tc)
      Tf = Tc * 1.8 + 32 # Convert to Farhenheit
      print('Tf : %.2f' %Tf)
      time.sleep(2)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832_2.destroy()