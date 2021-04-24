import datetime

class Data:
    def __init__(self, data: datetime, tmin: float, tmax: float, rain: float, temperatura: float, precipitazioni: float, venti: dict, radiazione: float, umidita_relativa: float)
        self.data = data
        self.tmin = tmin
        self.tmax = tmax
        self.rain = rain
        self.temperatura = temperatura
        self.precipitazioni = precipitazioni
        self.venti = venti
        self.radiazione = radiazione
        self.umidita_relativa = umidita_relativa

class Vento:
    def __init__(self, v: float, d: float):
        self.v = v
        self.d = d

# TODO decide hw to structure from xml to  -> ?