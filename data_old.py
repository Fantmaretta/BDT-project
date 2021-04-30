import datetime

class Vento:
    def __init__(self, v: float, d: float):
        self.v = v
        self.d = d

class Data:
    def __init__(self, data: datetime, tmin: float, tmax: float, rain: float, temperatura: dict, precipitazioni: dict, venti: dict, radiazione: dict, umidita_relativa: dict):
        self.data = data
        self.tmin = tmin
        self.tmax = tmax
        self.rain = rain
        self.temperatura = temperatura
        self.precipitazioni = precipitazioni
        self.venti = venti
        self.radiazione = radiazione
        self.umidita_relativa = umidita_relativa



# TODO decide hw to structure from xml to  -> ?