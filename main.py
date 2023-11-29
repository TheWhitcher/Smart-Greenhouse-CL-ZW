# Name:     main.py
# By:       Christophe Landry & Zacharyah Whitcher
# Date:     2023-04-28
# Version:  1.0

# Imports
import temperature_monitor
import uv_light_monitor
import soil_moisture_monitor
import time
import threading
import RPi.GPIO as GPIO

# Global Variables
waterpump_runtime = 10
waterpump_cooldown = 30
min_moisture = 10

# Do not need atm
# max_temp = 0
# min_temp = 0
# max_moisture = 0
# max_uv = 0
# min_uv = 0

# Setup the Components
def setup():
	soil_moisture_monitor.setup()
	temperature_monitor.setup()
	uv_light_monitor.setup()
	
def loop():
	global waterpump_runtime

	while True:
		# Get Sensor readings
		temperature = temperature_monitor.readSensor()
		moisture = soil_moisture_monitor.readSensor()
		light = uv_light_monitor.readSensor()
		print("+-----------------------------------------------+")
		print("| Type       Actual ")
		print("| Temp	    " + str(temperature))
		print("| Humidity   " + str(moisture))
		print("| Light	    " + str(light))
		print("+-----------------------------------------------+")
		
		# Run the sprinkler for 10 seconds with a 30 second cooldown
		if(moisture <= min_moisture and (time.monotonic() - waterpump_runtime) >= waterpump_cooldown):
			water_pump_thread = threading.Thread(target=soil_moisture_monitor.RunPump)
			water_pump_thread.start()
			waterpump_runtime = time.monotonic()
			
		time.sleep(0.5)
		
# Cleans up GPIO
def destroy():
	GPIO.cleanup()
	
# Main Program
if __name__ == '__main__':
	setup()

	try:
		loop()
	except KeyboardInterrupt: 
		destroy()
		print ('\nGoodbye! :)')
	finally:
		destroy()
