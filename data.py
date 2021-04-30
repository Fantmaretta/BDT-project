import datetime
import mysql.connector
from typing import Optional, List


class Vento:
    def __init__(self, v: float, d: float):
        self.v = v
        self.d = d

class Data:
    def __init__(self, data: datetime, tmin: float, tmax: float, rain_tot: float, temperatura: float, precipitazioni: float, vento_suolo: Vento):
        self.data = data
        self.tmin = tmin
        self.tmax = tmax
        self.rain_tot = rain_tot
        self.temperatura = temperatura
        self.precipitazioni = precipitazioni
        self.vento_suolo = vento_suolo


class MySQLStationManager:

    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            database="bdt-station-db",
            user="root",
            password="password"
        )
        self.connection.autocommit = True

    def save(self, stations: List[Data]) -> None:
        cursor = self.connection.cursor()
        query = "INSERT into data (data, tmin, tmax, rain_tot, temperatura, precipitazioni, vento_suolo) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        for station in stations:
            cursor.execute(query, (
                station.id,
                station.name,
                station.address,
                station.position.lat,
                station.position.lon,
                station.city,
                station.slots,
                station.bikes,
                station.dt.isoformat()
            ))

        cursor.close()

    def list(self) -> List[Station]:
        cursor = self.connection.cursor()
        query = "SELECT station_id, name, address, lat, lon, city, slots, bikes, timestamp from station"
        cursor.execute(query)

        stations = []
        for station_id, name, address, lat, lon, city, slots, bikes, timestamp in cursor:
            stations.append(Station(
                station_id,
                name,
                address, bikes, slots, city,
                Position(lat, lon),
                datetime.fromisoformat(timestamp)
            ))

        cursor.close()

        return stations

# TODO decide hw to structure from xml to  -> ?