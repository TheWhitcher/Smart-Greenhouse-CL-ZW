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
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import RPi.GPIO as GPIO

# Global Variables
waterpump_cooldown = 10
min_moisture = 10

# Do not need atm
# max_temp = 0
# min_temp = 0
# max_moisture = 0
# max_uv = 0
# min_uv = 0

# Setup the Components
def setup():
	# Setup Sensors
	soil_moisture_monitor.setup()
	temperature_monitor.setup()
	uv_light_monitor.setup()

# MQTT config (clientID must be unique within the AWS account)
clientID = "726084275207" #To be changed
endpoint = "ajkrqd5g9a48e-ats.iot.us-east-1.amazonaws.com" #To be changed // Use the endpoint from the settings page in the IoT console 
port = 8883 #Might need to be changed // MQTT port
topic = "raspberry/templight" #MIght need to be changed // Name of the topic to publish to in the IoT console 

# Init MQTT client
# mqttc = AWSIoTMQTTClient(clientID)
# mqttc.configureEndpoint(endpoint,port)
# mqttc.configureCredentials("certs/AmazonRootCA1.pem","certs/raspberry-private.pem.key","certs/raspberry-certificate.pem.crt")

# Send message to MQTT
# def send_data(message):
# 	mqttc.publish(topic,json.dumps(message),0)
# 	print("Message Published: " + message)

# Main Loop every 1 second
def loop():
	global waterpump_cooldown
	global min_moisture
	
	# Main loop
	while True:
		# Get Sensor readings
		temperature = temperature_monitor.readSensor()
		moisture = soil_moisture_monitor.readSensor()
		light = uv_light_monitor.readSensor()
		print("+-----------------------------------------------+")
		print("| Type       Actual ")
		print("| Temp	    "  + str(temperature))
		print("| Humidity   "  + str(moisture))
		print("| Light	    "+ str(light))
		print("+-----------------------------------------------+")
		
		# Run the sprinkler for 10 seconds
		if(moisture <= min_moisture and (time.monotonic() - waterpump_cooldown) >= 60):
			# Start a new thread to run the motor concurrently
			water_pump_thread = threading.Thread(target=soil_moisture_monitor.RunPump)
			water_pump_thread.start()
			waterpump_cooldown = time.monotonic()
			
		time.sleep(0.5)
		
# Cleans up GPIO
def destroy():
	GPIO.cleanup()
	
# Main Program
if __name__ == '__main__':
	setup()
	try:

		#Connect to MQTT
		#mqttc.connect()
		#print("Connect OK!")
		loop()
	except KeyboardInterrupt: 
		destroy()
		print ('\nThe end!')
	finally:
		destroy()
