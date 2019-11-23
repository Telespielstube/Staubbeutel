import sqlite3
from sqlite3 import Error
import datetime 

# SQLite DB Name
DB_Name =  "/Users/marta/SQLite/SensorDb.db"

class DatabaseManager():
	def __init__(self):
		self.connection = sqlite3.connect(DB_Name)
		self.connection.execute('pragma foreign_keys = on')
		self.connection.commit()
		# self.cursor = self.connection.cursor()
		
	def add_db_record(self, sql_query, args=()):
		cursor = self.connection.cursor()
		try:
		    cursor.execute(sql_query, args)
		except Error as e:
			print(e)
		self.connection.commit()
		return

	def __del__(self):
		self.connection.close()

	def parse_payload(self, payload):
		splitted_payload = payload.split(',')
		return splitted_payload[0], splitted_payload[1]

	def sensor_Data_Handler(self, topic, payload):
		if topic == '/home/backyard/dht11':
			decoded_payload = payload.decode('UTF-8')
			value1, value2 = self.parse_payload(str(decoded_payload))
			self.dht11_temperature_data(value1, value2)	
		if topic is "home/backyard/sds11":
			decoded_payload = payload.decode('UTF-8')
			value1, value2 = self.parse_payload(str(decoded_payload))
			self.sds11_dust_data(value1, value2)

	# Function to save temperature/ humididty values to DB Table
	def dht11_temperature_data(self, temperature, humidity):
		#Push into DB Table
		today = self.get_date()
		db_object = DatabaseManager()
		db_object.add_db_record("INSERT INTO dht11 (date, temperature, humidity, measuring_id) VALUES (?, ?, ?,?)", (today, temperature, humidity, 1))
		del db_object # function to delete an object.
		print ("Inserted Temperature Data.")
		print ("")

	# # Function to save dust values to DB Table
	def sds11_dust_data(self, pm10, pm25):
		#Push into DB Table
		today = self.get_date()
		db_object = DatabaseManager()
		db_object.add_db_record("INSERT INTO sds11 (date, pm10, pm25, measuring_id) VALUES (?, ?, ?,?)", (today, pm10, pm25, 1))
		del db_object 
		print ("Inserted Humidity Data.")
		print ("")

	def get_date(self):
		return (datetime.date.today()).strftime("%d-%m-%Y %H:%M:%S:%f")
	