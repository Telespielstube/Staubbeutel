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
        self.cursor = self.connection.cursor()

    # Inserts data into tables.
    #
    # sql_query     SQL query (INSERT INTO, SELECT FROM...)
    # args          vValues to be entered or called in the table
    def add_db_record(self, sql_query, args=()):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_query, args)
            last_id = self.cursor.lastrowid
            self.connection.commit()
            cursor.close()
        except Error as e:
            print(e)
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
            cursor.close()
        except Error as e:
            print("Sql file could not be read, because of:")
            print(e)

    # Splits the message payload into substrings.
    #
    # payload   message content
    def parse_payload(self, payload):
        splitted_payload = payload.split(',')
        return splitted_payload[0], splitted_payload[1]

    # Chooses the appropriate function based on the topic.
    #
    # topic     Topic on which was the message was published
    # payload   message content
    def sensor_data_handler(self, topic, payload):
        station_id = self.station.add_station(self.station.station_name)
        if topic == '/home/backyard/dht11':
            temperature, humidity = self.parse_payload(str(payload))
            self.temperature.dht11_temperature_sample(temperature, humidity, station_id)	
        if topic == '/home/backyard/sds11':
            pm10, pm25 = self.parse_payload(str(payload))
            self.finedust.sds11_dust_sample(pm10, pm25, station_id)