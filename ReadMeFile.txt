   ____                       _   _                        _ 
  / ___|_ __ ___  ___ _ __   | | | | ___  _   _ ___  ___  | |
 | |  _| '__/ _ \/ _ \ '_ \  | |_| |/ _ \| | | / __|/ _ \ | |
 | |_| | | |  __/  __/ | | | |  _  | (_) | |_| \__ \  __/ |_|
  \____|_|  \___|\___|_| |_| |_| |_|\___/ \__,_|___/\___| (_)
                                                             

  ____                _   __  __        _____ _ _          
 |  _ \ ___  __ _  __| | |  \/  | ___  |  ___(_) | ___   _ 
 | |_) / _ \/ _` |/ _` | | |\/| |/ _ \ | |_  | | |/ _ \ (_)
 |  _ <  __/ (_| | (_| | | |  | |  __/ |  _| | | |  __/  _ 
 |_| \_\___|\__,_|\__,_| |_|  |_|\___| |_|   |_|_|\___| (_)
                                                           


Welcome to the Internet of Things Green House read me file!

*********************************************************************************************

If you want to have you own smart green house you will need the following:

-Raspberry Pie 4 computer
-A breadboard
-Two ADC 0832
-One Soil Moisture Sensor
-One Light Sensor
-One Temperature Sensor
-One LED Light
-One Fan
-One Water Pump
-One Relay

********************************************************************************************

To build the green house the components need to be connected to the following GPIO on the breadboard.

-ADC 1: CS: Vcc: CLK: DO: DI:
-ADC 2: CS: Vcc: CLK: DO: DI:
-Soil Moisture Sensor & CM: Chanel 0 of ADC1  
-Light Sensor: Chanel 1 of ADC1
-Temperature Sensor: Chanel 0 of ADC2
-LED Light: GPIO 27
-Fan: GPIO 14
-Relay: 
-Water Pump:

*******************************************************************************************

To Start the Green House on you will need to do the following:

1-install mosquitto-client:
	sudo apt-get install curl mosquitto-clients
2-install python dot env:
	pip install python-dotenv
