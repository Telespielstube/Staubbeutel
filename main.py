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
parser.add_argument("-p", default = "/Users/marta/SQLite/Staubbeutel.db", required = False, help = "path where the local SQLite database is stored. Ex.: python3 main.py -p /Users/marta/Staubbeutel.db")
args = parser.parse_args()
db_path = args.p
if db_path is None:
	db_path = parser.get_default('p')
if not os.path.exists(db_path):
	with open(db_path, 'w'):
		pass
db = DatabaseManager(db_path)

#Broker credentials
mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883
keep_alive_interval = 60
mqtt_username = "telespielstube"
mqtt_password = "12345"
mqtt_topic = "/home/backyard/#" #subscribes to all messges of a topic that begins with pattern before the wildcard

# Called when broker responds to clients connection request.
#
# client	client instance for this callback.
# userdata	private user data like username, password
# flags		response flags sent by the broker
# rc		connection result. 
def on_connect(client, userdata, flags, rc):
	if rc is 0:
		print("Connected to broker")		
	mqttc.subscribe(mqtt_topic, 0)
	print("Subcribed")

# Called when broker responds to client subsscribe request.
#
# client	client instance for this callback.
# userdata	private user data like username, password
# mid		message id.
# qos		quality of service level.
def on_subscribe(client, userdata, mid, qos):
	print("Subscribed: " + str(mid) + " " + str(qos))

# The callback for when a PUBLISH message is received from the server.
#
# client	client instance for this callback.
# userdata	private user data like username, password
# message	message content.
def on_message(client, userdata, message):
	db.sensor_data_handler(str(message.topic), str(message.payload.decode('utf-8')))

# Callback function for disconnection
#
# client	client instance for this callback.
# userdata	private user data like username, password
# rc		connection result. 
def on_disconnect(client, userdata, rc):
    if rc is not 0:
        print("Unexpected disconnection from broker.")

connected = False
mqttc = mqtt.Client("Staubbeutel")
# Sets callback function to connect to broker and subcribe
mqttc.username_pw_set(mqtt_username, mqtt_password)
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message


try:
	mqttc.connect(mqtt_broker, mqtt_port, keep_alive_interval)
except Error as ex:
	print("Error occured while connecting to broker. Due to: \n")
	print(ex)
	connected = False

# Continue the network loop
mqttc.loop_forever()