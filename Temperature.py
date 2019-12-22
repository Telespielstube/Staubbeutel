from Date import Date

class Temperature():
    def __init__(self, DatabaseManager):
        self.db = DatabaseManager
        self.date = Date()

    # Function to save temperature/ humididty values to DB Table
    def dht11_temperature_sample(self, temperature, humidity, station_id):
        #Insert sensor data into database table
        now = self.date.get_date()
        date_id = self.db.add_db_record("INSERT INTO date (year, month, day, hour, minute) VALUES (?, ?, ?, ?, ?)", (now.year, now.month, now.day, now.hour, now.minute)) 
        self.db.add_db_record("INSERT INTO dht11 (temperature, humidity, date_id, station_id) VALUES (?, ?, ?, ?)", (temperature, humidity, date_id, station_id))
        self.db.connection.close()
        print ("Inserted temperature data.\n")