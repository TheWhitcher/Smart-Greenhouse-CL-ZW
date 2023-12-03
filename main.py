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

max_temp = 30
min_temp = 20

max_moisture = 50
min_moisture = 20

max_light = 100
min_light = 20

fan_override = False
water_pump_override = False

# MQTT config (clientID must be unique within the AWS account)
clientID = "726084275207" #To be changed
endpoint = "ajkrqd5g9a48e-ats.iot.us-east-1.amazonaws.com" #To be changed // Use the endpoint from the settings page in the IoT console 
port = 8883 #Might need to be changed // MQTT port
uplink_topic = "tb/aws/iot/smart-greenhouse/sensors" #Might need to be changed // Name of the topic to publish to in the IoT console 
downlink_topic = 'tb/aws/downlink'

# Init MQTT client
mqttc = AWSIoTMQTTClient(clientID)
mqttc.configureEndpoint(endpoint,port)
mqttc.configureCredentials("Smart-Greenhouse/certs/AmazonRootCA1.pem","Smart-Greenhouse/certs/raspberry-private.pem.key","Smart-Greenhouse/certs/raspberry-certificate.pem.crt")

# Send message to MQTT
def send_data(message):
	mqttc.publish(uplink_topic,json.dumps(message),0)
	print("Message Published: " + str(message))
	
# Define a callback function to handle incoming messages
def on_message(client, userdata, message):
	global fan_override
	global water_pump_override

	#print(f"Received message on topic {message.topic}: {message.payload}")

	# Decode the payload from bytes to a string
	payload_str = message.payload.decode("utf-8")

    # Parse the JSON payload
	payload_json = json.loads(payload_str)

    # Access the fan_override and water_pump_override values
	fan_override = payload_json.get("fan_override")
	water_pump_override = payload_json.get("water_pump_override")

# Setup the program
def setup():
	soil_moisture_monitor.setup()
	temperature_monitor.setup()
	uv_light_monitor.setup()

	# TODO: Uncomment before submitting
	# getTempInput()
	# getMoistureInput()
	# getLightInput()

# Setup the MQTTC connection
def setup_mqttc():

	print("\nConnecting to MQTT...")
	mqttc.connect()
	print("Connect OK!")

	print("Subscribing to dashboard...")
	#mqttc.onMessage = on_message
	mqttc.subscribe(downlink_topic, 1, on_message)
	print("Subscribed to ", downlink_topic)

# Get and validate user input to set the maximum temperature.
def getTempInput():
	global max_temp
	global min_temp

	while True:
		max_temp = input("\nSet maximum TEMPERATURE threshold (Default value: 30): ")

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
				print("Minimum temperature must be less than the Maximum temperature.")
		except:
			print("Invalid input, enter only whole numebrs.")

# Get and validate user input to set and minimum soil moisture.
def getMoistureInput():
	global max_moisture
	global min_moisture

	while True:
		max_moisture = input("\nSet maximum MOISTURE threshold between 1-100 (Default value: 50): ")

		try:
			max_moisture = int(max_moisture)

			if (max_moisture >= 1 and max_moisture <= 100):
				break
			else:
				print("Maximum moisture must be between 1 and 100.")
		except:
			print("Invalid input, enter only whole numebrs.")

	while True:
		min_moisture = input("\nSet minimum MOISTURE threshold between 1-100 (Default value: 20): ")

		try:
			min_moisture = int(min_moisture)

			if (min_moisture >= 1 and min_moisture < max_moisture):
				break

			if (min_moisture < 1):
				print ("Minimum moisture must be above 0.")
			elif (min_moisture > max_moisture):
				print ("Minimum moisture must be less than the maximum moisture.")
		except:
			print("Invalid input, enter only whole numebrs.")

# Get and validate user input to set and minimum soil moisture.
def getLightInput():
	global max_light
	global min_light

	while True:
		max_light = input("\nSet maximum LIGHT threshold between 1-100 (Default value: 100): ")

		try:
			max_light = int(max_light)

			if (max_light >= 1 and max_light <= 100):
				break
			else:
				print("Maximum light must be between 1 and 100.")
		except:
			print("Invalid input, enter only whole numebrs.")

	while True:
		min_light = input("\nSet minimum LIGHT threshold between 1-100 (Default value: 20): ")

		try:
			min_light = int(min_light)

			if (min_light >= 1 and min_light < max_light):
				break

			if (min_light < 1):
				print ("Minimum light must be above 0.")
			elif (min_light > max_light):
				print ("Minimum light must be less than the maximum light.")
		except:
			print("Invalid input, enter only whole numebrs.")

# Main loop
def loop():
	global waterpump_cooldown
	global fan_cooldown
	global min_moisture
	global fan_override
	global water_pump_override
	
	# Main loop
	while True:
		# Get Sensors readings
		temperature = temperature_monitor.readSensor()
		soil_moisture = soil_moisture_monitor.readSensor()
		uv_light_monitor.readSensor(max_light, min_light)

		message = {
			"val0": "loaded",
			"val1": str(temperature),
			"val2": str(soil_moisture),
			"val3": str(max_temp),
			"Val4": str(min_temp),
			"val5": str(max_moisture),
			"val6": str(min_moisture)
		}

		send_data(message)

		# Manually override the water pump.
		if(water_pump_override):
			soil_moisture_monitor.manualOverride(True)
		else:
			soil_moisture_monitor.manualOverride(False)
		
		# Run the water pump for 3 seconds
		if(not water_pump_override and soil_moisture < min_moisture and (time.monotonic() - waterpump_cooldown) >= 60):
			waterpump_thread = threading.Thread(target=soil_moisture_monitor.RunPump)
			waterpump_thread.start()
			waterpump_cooldown = time.monotonic()

		# Manually override the hvac system.
		if(fan_override):
			temperature_monitor.manualOverride(True)
		else:
			temperature_monitor.manualOverride(False)

		# Run the fan for 30 seconds
		if(not fan_override and temperature > max_temp and (time.monotonic() - fan_cooldown) >= 60):
			fan_thread = threading.Thread(target=temperature_monitor.RunLed) # Used for testing.
			#fan_thread = threading.Thread(target=temperature_monitor.RunFan)
			fan_thread.start()
			fan_cooldown = time.monotonic()
			
		time.sleep(2)
		
# Cleans up the GPIO
def destroy():
	GPIO.cleanup()
	
# Main Program
if __name__ == '__main__':
	setup()
	try:
		setup_mqttc()
		loop()
	except KeyboardInterrupt: 
		print('\nShutting Down...')
	finally:
		mqttc.disconnect()
		destroy()