import sqlite3 
import argparse
import sys
from sqlite3 import Error
import time
import os
import paho.mqtt.client as mqtt
from DatabaseManager import DatabaseManager

#Command line parser
parser = argparse.ArgumentParser()
parser.add_argument("-p", required=True, help="path where the local SQLite database is stored")

args = parser.parse_args()
db_path = args.p
if not os.path.exists(db_path):
	with open(db_path, 'w'):
		pass

#Broker credentials
mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883
keep_alive_interval = 60
mqtt_username = "telespielstube"
mqtt_password = "12345"
mqtt_topic = "/home/backyard/#" #subscribes to all messges of a topic that begins with pattern before the wildcard
db = DatabaseManager(db_path)


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
	print("Error occured while connecting to broker. Due to: \n")
	print(ex)
	connected = False

mqttc.loop_start()
while connected is not True:
	time.sleep(.5)
	mqttc.subscribe(mqtt_topic)

# Continue the network loop
mqttc.loop_forever()