from Date import Date

class Finedust():
    def __init__(self, DatabaseManager):
        self.db = DatabaseManager
        self.date = Date()

    # Function to save dust values to DB Table
    #
    # pm10          pm10 value
    # pm25          pm25 value
    # station_id    identification of the station.
    def sds11_dust_sample(self, pm10, pm25, station_id):
        now = self.date.get_date()
        self.db.add_db_record("INSERT INTO sds11 (pm_10, pm_25, timestamp, station_id) VALUES (?, ?, ?, ?)", (pm10, pm25, now, station_id))
        print ("Inserted fine dust data.\n")