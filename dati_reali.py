import datetime
import mysql.connector
from typing import Optional, List


class Vento:
    def __init__(self, v: float, d: float):
        self.v = v
        self.d = d

class DatiReali:
    def __init__(self, station_code: str, localita: str, data: datetime.date, time: datetime.time, temperatura: float, pioggia: float, vento: Vento):
        self.station_code = station_code
        self.localita = localita
        self.data = data
        self.time = time
        self.temperatura = temperatura
        self.pioggia = pioggia
        self.vento = vento

    def to_repr(self) -> dict:
        return {
            "station_code": self.station_code,
            "localita": self.localita,
            "data": self.data,
            "time": self.time,
            "temperatura": self.temperatura,
            "pioggia": self.pioggia,
            "vento_velocita": self.vento.v,
            "vento_direzione": self.vento.d
        }

    @staticmethod
    def from_repr(raw_data: dict):
        return DatiReali(
            raw_data["station_code"],
            raw_data["localita"],
            raw_data["data"],
            raw_data["time"],
            raw_data["temperatura"],
            raw_data["pioggia"],
            Vento(
                raw_data["vento_velocita"],
                raw_data["vento_direzione"]
            )
        )


class MySQLDatiRealiManager:

    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            host="bdtmysql.cvpe8im7hapy.us-east-2.rds.amazonaws.com",
            port=3306,
            database="bdt_db_mysql",
            user="root_bdt",
            password="bdt_mysql"
        )
        self.connection.autocommit = True

    def save(self, dati_reali: List[List[DatiReali]]) -> None:
        cursor = self.connection.cursor()
        query = "INSERT into dat_reali (station_code, localita, data, time, temperatura, pioggia, vento_velocita, vento_direzione)" \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        for dato_list in dati_reali:
            for dato in dato_list:
                cursor.execute(query, (
                    dato.station_code,
                    dato.localita,
                    dato.data,
                    dato.time,
                    dato.temperatura,
                    dato.pioggia,
                    dato.vento.v,
                    dato.vento.d,
                ))

        cursor.close()

    def list(self) -> List[DatiReali]:
        cursor = self.connection.cursor()
        query = "SELECT station_code, localita, data, time, temperatura, pioggia, velocita_vento, direzione_vento from dati_reali"
        cursor.execute(query)

        dati_reali = []
        for station_code, localita, data, time, temperatura, pioggia, velocita_vento, direzione_vento in cursor:
            dati_reali.append(DatiReali(
                station_code,
                localita,
                data,
                temperatura,
                pioggia,
                Vento(
                    velocita_vento,
                    direzione_vento
                )
            ))

        cursor.close()

        return dati_reali

dati_reali_manager = MySQLDatiRealiManager()
# TODO decide hw to structure from xml to  -> ?