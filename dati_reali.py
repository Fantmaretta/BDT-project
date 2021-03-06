import datetime
import mysql.connector
from typing import List


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
        '''
        Represent a DatiReali object ad dictionary
        :return:
        '''

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
        '''
        Represent a dictionary as a DatiReali object
        :param raw_data:
        :return:
        '''

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
        '''
        Connect to database Mysql
        '''

        self.connection = mysql.connector.connect(
            host="bdtmysql.cvpe8im7hapy.us-east-2.rds.amazonaws.com",
            port=3306,
            database="bdt_db_mysql",
            user="root_bdt",
            password="bdt_mysql"
        )
        self.connection.autocommit = True

    def save(self, dati_reali: List[List[DatiReali]]) -> None:
        '''
        Collect real data and save them into the database
        :param dati_reali:
        :return:
        '''

        cursor = self.connection.cursor()
        query = "INSERT into dati_reali (station_code, localita, data, time, temperatura, pioggia, vento_velocita, vento_direzione)" \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        i = 0
        for dato_list in dati_reali:
            #i += 1
            #print(i)
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
        '''
        Given attributes of DatiReali objects, create the objects and save them into a list
        :return:
        '''

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