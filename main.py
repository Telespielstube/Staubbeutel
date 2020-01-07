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
parser.add_argument("-p", default = "~/Staubbeutel_default.db", required = False, help = "path where the local SQLite database is stored. Ex.: python3 main.py -p /Users/marta/Staubbeutel.db")
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

def on_connect(hivemq, userdata, rc):
	print("Connected with result code " + str(rc))
	if rc is 0:
		print("Connected to broker")
		
	mqttc.subscribe(mqtt_topic, 0)
	print("Subcribed")

# When the broker has acknowledged the subscription, .
def on_subscribe(hivemq, obj, message_id, granted_qos):
    pass

# The callback for when a PUBLISH message is received from the server.
def on_message(hivemq, obj, message):
	print ("MQTT Data Received...")
	print ("MQTT Topic: " + str(message.topic))  
	print ("Data: " + str(message.payload.decode('UTF-8')))
	db.sensor_data_handler(str(message.topic), str(message.payload.decode('utf-8')))

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
	mqttc.subscribe(mqtt_topic, 0)

# Continue the network loop
mqttc.loop_forever()