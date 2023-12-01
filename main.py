# Name:     main.py
# By:       Christophe Landry & Zacharyah Whitcher
# Date:     2023-11-24
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
min_moisture = 10

# MQTT config (clientID must be unique within the AWS account)
clientID = "726084275207" #To be changed
endpoint = "ajkrqd5g9a48e-ats.iot.us-east-1.amazonaws.com" #To be changed // Use the endpoint from the settings page in the IoT console 
port = 8883 #Might need to be changed // MQTT port
topic = "tb/aws/iot/smart-greenhouse/sensors" #Might need to be changed // Name of the topic to publish to in the IoT console 

# Init MQTT client
mqttc = AWSIoTMQTTClient(clientID)
mqttc.configureEndpoint(endpoint,port)
mqttc.configureCredentials("Smart-Greenhouse/certs/AmazonRootCA1.pem","Smart-Greenhouse/certs/raspberry-private.pem.key","Smart-Greenhouse/certs/raspberry-certificate.pem.crt")

# Setup the program
def setup():
	soil_moisture_monitor.setup()
	temperature_monitor.setup()
	uv_light_monitor.setup()

	getTempInput()
	getMoistureInput()

# Get and validate user input to set the maximum temperature.
def getTempInput():
	global max_temp

	while True:
		max_temp = input("\nSet maximum TEMPERATURE threshold (Default value: 35): ")

		try:
			max_temp = int(max_temp)
			break
		except:
			print("Invalid input, enter only whole numebrs.")

# Get and validate user input to set and minimum soil moisture.
def getMoistureInput():
	global min_moisture

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

# Send message to MQTT
def send_data(message):
	mqttc.publish(topic,json.dumps(message),0)
	print("Message Published: " + str(message))

# Main loop
def loop():
	global waterpump_cooldown
	global fan_cooldown
	global min_moisture
	
	# Main loop
	while True:
		# Get Sensors readings
		temperature = temperature_monitor.readSensor()
		soil_moisture = soil_moisture_monitor.readSensor()
		uv_light_monitor.readSensor()

		message = {
			"val0": "loaded",
			"val1": str(temperature),
			"val2": str(soil_moisture)
		}

		send_data(message)
		
		# Run the water pump for 3 seconds
		if(soil_moisture < min_moisture and (time.monotonic() - waterpump_cooldown) >= 60):
			waterpump_thread = threading.Thread(target=soil_moisture_monitor.RunPump)
			waterpump_thread.start()
			waterpump_cooldown = time.monotonic()

		# Run the fan for 30 seconds
		if(soil_moisture <= min_moisture and (time.monotonic() - fan_cooldown) >= 60):
			fan_thread = threading.Thread(target=temperature_monitor.RunFan)
			fan_thread.start()
			fan_cooldown = time.monotonic()
			
		time.sleep(0.5)
		
# Cleans up the GPIO
def destroy():
	GPIO.cleanup()
	
# Main Program
if __name__ == '__main__':
	setup()
	try:
		#Connect to MQTT
		print("\nConnecting to MQTT...")
		mqttc.connect()
		print("Connect OK!\n")

		loop()
	except KeyboardInterrupt: 
		print('\nShutting Down...')
	# except:
	# 	print("\nFailed to connect to MQTT")
	finally:
		destroy()