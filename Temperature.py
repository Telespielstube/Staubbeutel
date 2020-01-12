from Date import Date

class Temperature():
    def __init__(self, DatabaseManager):
        self.db = DatabaseManager
        self.date = Date()

    # Function to save temperature/ humididty values to DB Table
    #
    # temperature   temerature value
    # humidity      humidity value
    # station_id    identification of the station
    def dht11_temperature_sample(self, temperature, humidity, station_id):
        now = self.date.get_date()   
        self.db.add_db_record("INSERT INTO dht11 (temperature, humidity, timestamp, station_id) VALUES (?, ?, ?, ?)", (temperature, humidity, now, station_id))
        print ("Inserted temperature data.\n")