import sqlite3 
from sqlite3 import Error
import time
import sys
import paho.mqtt.client as mqtt
from DatabaseManager import DatabaseManager

#Broker credentials
mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883
keep_alive_interval = 60
mqtt_username = "telespielstube"
mqtt_password = "12345"
mqtt_topic = "/home/backyard/#" #subscribes to all messges of a topic that begins with pattern before the wildcard
db = DatabaseManager()


def on_connect(hivemq, obj, rc):
	print("Connected with result code " + str(rc))
	if rc is 0:
		print("Connected to broker")
	
	mqttc.subscribe(mqtt_topic, 0)
	print("Subcribed")

#Save Data into DB Table
def on_message(hivemq, obj, message):
	print ("MQTT Data Received...")
	print ("MQTT Topic: " + str(message.topic))  
	print ("Data: " + str(message.payload))
	
	db.sensor_Data_Handler(str(message.topic), message.payload)

def on_subscribe(hivemq, obj, mid, granted_qos):
    pass

connected = False
mqttc = mqtt.Client("Staubbeutel")
# Connect to broker and subcribe
mqttc.username_pw_set(mqtt_username, mqtt_password)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
try:
	mqttc.connect(mqtt_broker, mqtt_port, keep_alive_interval)
except Error as ex:
	print("Could not connect to broker. Due to: \n")
	print(ex)
	connected = False

mqttc.loop_start()
while connected is not True:
	time.sleep(.5)
	mqttc.subscribe(mqtt_topic)

# Continue the network loop
mqttc.loop_forever()