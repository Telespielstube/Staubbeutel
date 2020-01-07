BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "station" (
	"station_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"station_name"	TEXT
);
CREATE TABLE IF NOT EXISTS "sds11" (
	"sds_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"pm_10"	TEXT,
	"pm_25"	TEXT,
	"timestamp"	TEXT,
	"station_id"	INTEGER NOT NULL,
	FOREIGN KEY("station_id") REFERENCES "station"("station_id")
);
CREATE TABLE IF NOT EXISTS "dht11" (
	"dht_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"temperature"	TEXT,
	"humidity"	TEXT,
	"timestamp"	TEXT,
	"station_id"	INTEGER NOT NULL,
	FOREIGN KEY("station_id") REFERENCES "station"("station_id")
);
COMMIT;
