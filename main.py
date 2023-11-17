# Name:     main.py
# By:       Christophe Landry & Zacharyah Whitcher
# Date:     2023-04-28
# Version:  1.0

# Imports
from tkinter import *
import os
import GreenHouseGUI
import temperature_monitor
import uv_light_monitor
import soil_moisture_monitor
import time
import threading

# Global Variables
water_cooldown = 0

# Setup the Components
def setup():
	# Setup Sensors
	soil_moisture_monitor.setup()
	temperature_monitor.setup()
	uv_light_monitor.setup()
	
	# Setup GUI
	def on_closing():
		app.master.withdraw()
        
	global app
	root=Tk()
	root.title('Greenhouse GUI')
	root.geometry('430x170')
	app = GreenHouseGUI.Application(root)
	
	root.protocol("WM_DELETE_WINDOW", on_closing)
	
	# Default values
	global max_temp
	max_temp = float(app.tempMax.cget("text"))
	
	global min_temp
	min_temp = float(app.tempMin.cget("text"))
	
	global max_moisture
	max_moisture = float(app.soilMax.cget("text"))
	
	global min_moisture
	min_moisture = float(app.soilMin.cget("text"))
	
	global max_uv
	max_uv = float(app.uvMax.cget("text"))
	
	global min_uv
	min_uv = float(app.uvMin.cget("text"))
	
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
		temperature = temperature_monitor.readSensors(max_temp, min_temp)
		moisture = soil_moisture_monitor.readSensor(max_moisture, min_moisture)
		light = uv_light_monitor.readSensor(max_uv, min_uv)
		print("+-----------------------------------------------+")
		print("| Type       Min      Max      Actual ")
		print("| Temp	     " + str(min_temp) + "     " + str(max_temp) + "     " + str(temperature))
		print("| Humidity   " + str(min_moisture) + "     " + str(max_moisture) + "     " + str(moisture))
		print("| Light	     " + str(min_uv) + "     " + str(max_uv) + "    " + str(light))
		print("+-----------------------------------------------+")
		
		# Update GUI Labels
		app.tempActual.config(text=str(temperature))
		app.soilActual.config(text=str(moisture))
		app.uvActual.config(text=str(light))
		
		# Detemine GUI Label colors
		actualFG(app.tempActual, temperature, max_temp, min_temp)
		actualFG(app.soilActual, moisture, max_moisture, min_moisture)
		actualFG(app.uvActual, light, max_uv, min_uv)
		
		# Update GUI
		app.update_idletasks()
		app.update()
		#app.mainloop()
		
		# Update values
		max_temp = float(app.tempMax.cget("text"))
		min_temp = float(app.tempMin.cget("text"))
		max_moisture = float(app.soilMax.cget("text"))
		min_moisture = float(app.soilMin.cget("text"))
		max_uv = float(app.uvMax.cget("text"))
		min_uv = float(app.uvMin.cget("text"))
		
		# Run the sprinkler for 10 seconds
		if(moisture <= min_moisture and (time.monotonic() - water_cooldown) >= 60):
			# Start a new thread to run the motor concurrently
			t = threading.Thread(target=soil_moisture_monitor.RunMotor)
			t.start()
			water_cooldown = time.monotonic()
			
		time.sleep(0.5)
		
# Change the foreground color of the Actual values
def actualFG(label, value, max, min):
	if ( value <= max and value >= min):
		label.config(fg = "green")
	else:
		label.config(fg = "red")
		
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
	print ('The end !')
finally:
	destroy()
