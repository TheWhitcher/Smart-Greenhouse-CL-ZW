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

# Fan Pins
FAN = 4

# Global Variables
fan_cooldown = False

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(FAN, GPIO.OUT)
	GPIO.output(FAN, GPIO.LOW)
	ADC0832_2.setup()

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

# Run the Fan
def RunFan():
	global fan_cooldown
	
	if(not fan_cooldown):
		fan_cooldown = True
		handleFan(True)
		time.sleep(30)
		handleFan(False)
		fan_cooldown = False

# Turn the fan on or off
def handleFan(status=False):
	if (status): # stop
		GPIO.output(FAN, GPIO.HIGH)
	else:
		GPIO.output(FAN, GPIO.LOW)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832_2.destroy()