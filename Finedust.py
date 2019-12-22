from Date import Date

class Finedust():
    def __init__(self, DatabaseManager):
        self.db = DatabaseManager
        self.date = Date()

    # Function to save dust values to DB Table
    def sds11_dust_sample(self, pm10, pm25, station_id):
        now = self.date.get_date()
        date_id = self.db.add_db_record("INSERT INTO date (year, month, day, hour, minute) VALUES (?, ?, ?, ?, ?)", (now.year, now.month, now.day, now.hour, now.minute))
        self.db.add_db_record("INSERT INTO sds11 (pm_10, pm_25, date_id, station_id) VALUES (?, ?, ?, ?)", (pm10, pm25, date_id, station_id))
        self.db.connection.close()
        print ("Inserted fine dust data.\n")