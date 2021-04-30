import datetime

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



# TODO decide hw to structure from xml to  -> ?