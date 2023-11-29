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

# Global Variables
water_cooldown = 0
max_temp = 0
min_temp = 0
max_moisture = 0
min_moisture = 10
max_uv = 0
min_uv = 0

# Setup the Components
def setup():
	# Setup Sensors
	soil_moisture_monitor.setup()
	temperature_monitor.setup()
	uv_light_monitor.setup()
	
# Main Loop every 1 second
def loop():
	global water_cooldown
	global max_temp
	global min_temp
	global max_moisture
	global min_moisture
	global max_uv
	global min_uv
	
	# Main loop
	while True:
		# Get Sensor readings
		temperature = temperature_monitor.readSensor()
		moisture = soil_moisture_monitor.readSensor()
		light = uv_light_monitor.readSensor(max_uv, min_uv)
		print("+-----------------------------------------------+")
		print("| Type       Min      Max      Actual ")
		print("| Temp	     " + str(min_temp) + "     " + str(max_temp) + "     " + str(temperature))
		print("| Humidity   " + str(min_moisture) + "     " + str(max_moisture) + "     " + str(moisture))
		print("| Light	     " + str(min_uv) + "     " + str(max_uv) + "    " + str(light))
		print("+-----------------------------------------------+")
		
		# Run the sprinkler for 10 seconds
		if(moisture <= min_moisture and (time.monotonic() - water_cooldown) >= 60):
			# Start a new thread to run the motor concurrently
			water_pump_thread = threading.Thread(target=soil_moisture_monitor.RunMotor)
			water_pump_thread.start()
			water_cooldown = time.monotonic()
			
		time.sleep(0.5)
		
# Cleans up GPIO
def destroy():
	soil_moisture_monitor.destroy()
	temperature_monitor.destroy()
	uv_light_monitor.destroy()
	
# Main Program
if __name__ == '__main__':
	setup()
try:
	loop()
except KeyboardInterrupt: 
	destroy()
	print ('The end!')
finally:
	destroy()
