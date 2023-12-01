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
waterpump_cooldown = 3
fan_cooldown = 30
max_temp = 35
min_temp = 20
min_moisture = 10

# Setup the Components
def setup():
	global max_temp
	global min_temp
	global min_moisture

	soil_moisture_monitor.setup()
	temperature_monitor.setup()
	uv_light_monitor.setup()

	while True:
		max_temp = input("\nSet maximum TEMPERATURE threshold (Default value: 35): ")

		try:
			max_temp = int(max_temp)
			break
		except:
			print("Invalid input, enter only whole numebrs.")

	while True:
		min_temp = input("\nSet minimum TEMPERATURE threshold (Default value: 20): ")

		try:
			min_temp = int(min_temp)

			if (min_temp < max_temp):
				break
			else:
				print("Minimum temperature must be greater than maximum temperature")
		except:
			print("Invalid input, enter only whole numebrs.")

	while True:
		min_moisture = input("\nSet minimum MOISTURE threshold between 1-100 (Default value: 10): ")

		try:
			min_moisture = int(min_moisture)

			if (min_moisture < 1):
				min_moisture = 1
			elif (min_moisture > 100):
				min_moisture = 100

			break
		except:
			print("Invalid input, enter only whole numebrs.")


# MQTT config (clientID must be unique within the AWS account)
clientID = "726084275207" #To be changed
endpoint = "ajkrqd5g9a48e-ats.iot.us-east-1.amazonaws.com" #To be changed // Use the endpoint from the settings page in the IoT console 
port = 8883 #Might need to be changed // MQTT port
topic = "cl-zw/smart-greenhouse" #Might need to be changed // Name of the topic to publish to in the IoT console 

# Init MQTT client
mqttc = AWSIoTMQTTClient(clientID)
mqttc.configureEndpoint(endpoint,port)
mqttc.configureCredentials("Smart-Greenhouse/certs/AmazonRootCA1.pem","Smart-Greenhouse/certs/raspberry-private.pem.key","Smart-Greenhouse/certs/raspberry-certificate.pem.crt")

# Send message to MQTT
def send_data(message):
	mqttc.publish(topic,json.dumps(message),0)
	print("Message Published: " + str(message))
	
def loop():
	global waterpump_cooldown
	global min_moisture
	
	# Main loop
	while True:
		print(max_temp)
		print(min_temp)
		# Get Sensors readings
		temperature = temperature_monitor.readSensor(max_temp, min_temp)
		soil_moisture = soil_moisture_monitor.readSensor()
		light = uv_light_monitor.readSensor()

		message = {
			"Temperature": str(temperature),
			"Light": str(light),
			"Soil Moisture": str(soil_moisture)
		}

		send_data(message)

		# print("+-----------------------------------------------+")
		# print("| Type       Actual ")
		# print("| Temp	    "  + str(temperature))
		# print("| Humidity   "  + str(soil_moisture))
		# print("| Light	    "+ str(light))
		# print("+-----------------------------------------------+")
		
		# Run the water pump for 10 seconds
		if(soil_moisture <= min_moisture and (time.monotonic() - waterpump_cooldown) >= 60):
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
		mqttc.connect()
		print("Connect OK!")

		loop()
	except KeyboardInterrupt: 
		destroy()
		print ('\nThe end!')
	finally:
		destroy()