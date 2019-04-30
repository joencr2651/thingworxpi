import os 
import time 
import requests
import psutil
import socket

sense = SenseHat() 
sense.set_rotation(180)

urlbase = 'https://twx.studio-trial.vuforia.io/Thingworx/Things/' 
thing = 'RaspberryPi1%2528c45f2ff14c5067f4%2529' 
tempProperty = 'Prop_Temperature' 
humidityProperty = 'Prop_Humidity'
coreTempProperty = 'Core_Temperature'
totalMemProperty = 'Total_Memory'
usedMemProperty = 'Used_Memory'
hostnameProperty = 'Hostname'
blue = (72,61,139)
green = (50,205,50)
yellow = (255,255,0)

appkey = '393cb60e-0367-49ab-b0a1-1468339b331b' 

headers = {
	'appKey': appkey,
	'Accept': "application/json",
	'Content-Type': "application/json",
}

def read_sensors():
#	sense.show_message("Data", text_colour=blue)
	temp_c = sense.get_temperature()
	temp_f = round(temp_c*9.0/5.0+32.0, 2)
	humidity = round(sense.get_humidity(), 2)
#	pressure = round(sense.get_pressure(), 2)
	coreTemp = psutil.sensors_temperatures().coretemp
	totalMemory = psutil.virtual_memory()[0]
	usedMemory = psutil.virtual_memory()[3]
	hostname = socket.gethostname()

	urlTemp = urlbase + thing + '/Properties/' + tempProperty
	urlHum = urlbase + thing + '/Properties/' + humidityProperty
	urlTotMem = urlbase + thing + '/Properties/' + totalMemProperty
	urlUsedMem = urlbase + thing + '/Properties/' + usedMemProperty
	urlHostname = urlbase + thing + '/Properties/' + hostnameProperty	
	urlCoreTemp = urlbase + thing + '/Properties/' + coreTempProperty		
	
	payloadTemp = "{\n\t\"" + tempProperty + "\": \"" + str(temp_f) + "\"\n}"
	payloadHum = "{\n\t\"" + humidityProperty + "\": \"" + str(humidity) + "\"\n}"
	payloadTotMem = "{\n\t\"" + totalMemProperty + "\": \"" + str(totalMemory) + "\"\n}"
	payloadUsedMem = "{\n\t\"" + usedMemProperty + "\": \"" + str(usedMemory) + "\"\n}"
	payloadHostname = "{\n\t\"" + hostnameProperty + "\": \"" + hostname + "\"\n}"
	payloadCoreTemp = "{\n\t\"" + coreTempProperty + "\": \"" + str(coreTemp) + "\"\n}"
	
	response = requests.request("PUT", urlTemp, data=payloadTemp, headers=headers)
	response = requests.request("PUT", urlHum, data=payloadHum, headers=headers)
	response = requests.request("PUT", urlTotMem, data=payloadTotMem, headers=headers)
	response = requests.request("PUT", urlUsedMem, data=payloadUsedMem, headers=headers)
	response = requests.request("PUT", urlHostname, data=payloadHostname, headers=headers)
	response = requests.request("PUT", urlCoreTemp, data=payloadCoreTemp, headers=headers)	

	
#	sense.clear(blue)
#	time.sleep(0.30)
#	sense.clear(green)
#	time.sleep(0.30)
#	sense.clear(yellow)
#	time.sleep(0.30)
#	sense.clear()	
	return hostname, temp_f, humidity, coreTemp, totalMemory, usedMemory
		
while True:
	print(read_sensors())
	time.sleep(3)


	
