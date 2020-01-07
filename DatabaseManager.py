import sqlite3
from sqlite3 import Error
from Date import Date
from Station import Station
from Temperature import Temperature
from Finedust import Finedust

class DatabaseManager():
    def __init__(self, db_path):
        self.date = Date()
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.createTables()
        self.connection.execute('pragma foreign_keys = on')
        self.connection.commit()
        self.station = Station(self, 'backyard')
        self.temperature = Temperature(self)
        self.finedust = Finedust(self)

    def add_db_record(self, sql_query, args=()):      
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_query, args)
            last_id = cursor.lastrowid
            cursor.close()
        except Error as e:
            print(e)
        self.connection.commit()
        return last_id

    # Reads a script to create all tables needed for the database
    def createTables(self):
        print("Creating database tables...")
        try:
            with open('/Users/marta/Documents/Python/Staubbeutel/Staubbeutel.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            cursor = self.connection.cursor()
            cursor.executescript(sql_script)
            self.connection.commit()
        except Error as e:
            print("Sql file could not be read, because of:")
            print(e)
        print("Finished!")

    def parse_payload(self, payload):
        splitted_payload = payload.split(',')
        return splitted_payload[0], splitted_payload[1]

    def sensor_data_handler(self, topic, payload):
        if topic == '/home/backyard/#':
            station_id = self.station.add_station(self.station.station_name) 
        if topic == '/home/backyard/dht11':
            temperature, humidity = self.parse_payload(str(payload))
            self.temperature.dht11_temperature_sample(temperature, humidity, station_id)	
        if topic == '/home/backyard/sds11':
            pm10, pm25 = self.parse_payload(str(payload))
            self.finedust.sds11_dust_sample(pm10, pm25, station_id)