import datetime
import mysql.connector
from typing import Optional, List


class Vento:
    def __init__(self, v: float, d: float):
        self.v = v
        self.d = d

class DatoReale:
    def __init__(self, station_code: str, localita: str, data: datetime, time: datetime, temperatura: float, pioggia: float, vento: Vento):
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
        return DatoReale(
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

# TODO decide hw to structure from xml to  -> ?