class Station():
    def __init__(self, DatabaseManager, name):
        self._station_name = name
        self.db = DatabaseManager
        self.existing_id = 0

    @property
    def station_name(self):
        return self._station_name

    @station_name.setter
    def station_name(self, name):
        self._station_name = name

    def check_if_station_exists(self, name):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT station_id FROM station WHERE station_name=:name", {"name": name})
        row = cursor.fetchone()
        if row == None:
            return False
        else:
            self.existing_id = row[0]
            cursor.close()
            return True

    # Adds a station to the "station" table
    def add_station(self, name):
        station_id = 0
        if not self.check_if_station_exists(name):
            station_id = self.db.add_db_record("INSERT INTO station (station_name) VALUES (?)", (name,))
            return station_id
        else:
            station_id = self.existing_id
        return station_id
