from datetime import datetime
from typing import List
import mysql.connector


class Precipitazioni:

    def __init__(self, id_prec_prob: str, desc_prec_prob: str, id_prec_int: str, desc_prec_int: str):
        self.id_prec_prob = id_prec_prob
        self.desc_prec_prob = desc_prec_prob
        self.id_prec_int = id_prec_int
        self.desc_prec_int = desc_prec_int

class Vento:

    def __init__(self, id_alt: str, desc_alt: str, id_dir_alt: str, desc_dir_alt: str, id_val: str, desc_val: str,
                 id_dir_val: str, desc_dir_val: str):
        self.id_alt = id_alt
        self.desc_alt = desc_alt
        self.id_dir_alt = id_dir_alt
        self.desc_dir_alt = desc_dir_alt
        self.id_val = id_val
        self.desc_val = desc_val
        self.id_dir_val = id_dir_val
        self.desc_dir_val = desc_dir_val

class Previsione:

    def __init__(self, localita: str, data: datetime.date, id_previsione_giorno: int, temp_min: int, temp_max: int, fascia: str, precipitazioni: Precipitazioni, vento: Vento):
        self.localita = localita
        self.data = data
        self.id_previsione_giorno = id_previsione_giorno
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.fascia = fascia
        self.precipitazioni = precipitazioni
        self.vento = vento

    def to_repr(self) -> dict:
        '''
        Represent a Previsioni object as dictionary
        :return:
        '''

        return {
            "localita": self.localita,
            "data": self.data,
            "id_previsione_giorno": self.id_previsione_giorno,
            "temp_min": self.temp_min,
            "temp_max": self.temp_max,
            "facia": self.fascia,
            "id_prec_prob": self.precipitazioni.id_prec_prob,
            "desc_prec_prob": self.precipitazioni.desc_prec_prob,
            "id_prec_int": self.precipitazioni.id_prec_int,
            "desc_prec_int": self.precipitazioni.desc_prec_int,
            "id_alt": self.vento.id_alt,
            "desc_alt":self.vento.desc_alt,
            "id_dir_alt": self.vento.id_dir_alt,
            "desc_dir_alt": self.vento.desc_dir_alt,
            "id_val": self.vento.id_val,
            "desc_val": self.vento.desc_val,
            "id_dir_val": self.vento.id_dir_val,
            "desc_dir_val": self.vento.desc_dir_val
        }

    @staticmethod
    def from_repr(raw_pred: dict):
        '''
        Represent a dictionary as a Previsioni object
        :param raw_pred:
        :return:
        '''

        return Previsione(
            raw_pred["localita"],
            raw_pred["data"],
            raw_pred["id_previsione_giorno"],
            raw_pred["temp_min"],
            raw_pred["temp_max"],
            raw_pred["fascia"],
            Precipitazioni(
                raw_pred["id_prec_prob"],
                raw_pred["desc_prec_prob"],
                raw_pred["id_prec_int"],
                raw_pred["desc_prec_int"],
            ),
            Vento(
                raw_pred["id_alt"],
                raw_pred["desc_alt"],
                raw_pred["id_dir_alt"],
                raw_pred["desc_dir_alt"],
                raw_pred["id_val"],
                raw_pred["desc_val"],
                raw_pred["id_dir_val"],
                raw_pred["desc_dir_val"],
            )
        )

    def __eq__(self, o: object) -> bool:
        return super().__eq__(o)


class MysqlPrevisioniManager:

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

    def save(self, previsioni: List[Previsione]) -> None:
        '''
        Collect predictions and save them into the database
        :param previsioni:
        :return:
        '''

        cursor = self.connection.cursor()
        query = "INSERT into previsioni (localita, data, id_previsione_giorno, temp_min, temp_max, fascia, " \
                "id_prec_prob, desc_prec_prob, id_prec_int, desc_prec_int, id_vento_alt, desc_vento_alt, " \
                "id_vento_dir_alt, desc_vento_dir_alt, id_vento_val, desc_vento_val, id_vento_dir_val, desc_vento_dir_val) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        for previsione in previsioni:
            cursor.execute(query, (
                previsione.localita,
                previsione.data,
                previsione.id_previsione_giorno,
                previsione.temp_min,
                previsione.temp_max,
                previsione.fascia,
                previsione.precipitazioni.id_prec_prob,
                previsione.precipitazioni.desc_prec_prob,
                previsione.precipitazioni.id_prec_int,
                previsione.precipitazioni.desc_prec_int,
                previsione.vento.id_alt,
                previsione.vento.desc_alt,
                previsione.vento.id_dir_alt,
                previsione.vento.desc_dir_alt,
                previsione.vento.id_val,
                previsione.vento.desc_val,
                previsione.vento.id_dir_val,
                previsione.vento.desc_dir_val,
            ))

        cursor.close()

    def list(self) -> List[Previsione]:
        '''
        Given attributes of Previsioni objects, create the objects and save them into a list
        :return:
        '''

        cursor = self.connection.cursor()
        query = "SELECT localita, data, id_previsione_giorno, temp_min, temp_max, fascia, id_prec_prob, desc_prec_prob, " \
                "id_prec_int, desc_prec_int, id_vento_alt, desc_vento_alt, id_vento_dir_alt, desc_vento_dir_alt," \
                "id_vento_val, desc_vento_val, id_vento_dir_val, desc_vento_dir_val from previsioni"
        cursor.execute(query)

        previsioni = []
        for localita, data, id_previsione_giorno, temp_min, temp_max, fascia, id_prec_prob, desc_prec_prob, id_prec_int, desc_prec_int, id_vento_alt, desc_vento_alt, id_vento_dir_alt, desc_vento_dir_alt, id_vento_val, desc_vento_val, id_vento_dir_val, desc_vento_dir_val in cursor:
            previsioni.append(Previsione(
                localita,
                data,
                id_previsione_giorno,
                temp_min,
                temp_max,
                fascia,
                Precipitazioni(
                    id_prec_prob,
                    desc_prec_prob,
                    id_prec_int,
                    desc_prec_int,
                ),
                Vento(
                    id_vento_alt,
                    desc_vento_alt,
                    id_vento_dir_alt,
                    desc_vento_dir_alt,
                    id_vento_val,
                    desc_vento_val,
                    id_vento_dir_val,
                    desc_vento_dir_val)
            ))

        cursor.close()

        return previsioni


