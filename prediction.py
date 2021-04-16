from typing import List


class Icon:

    def __init__(self, id_icon: int, icon: str, desc_icon: str):
        self.id_icon = id_icon
        self.id_icon = icon
        self.desc_icon = desc_icon

class Rain:

    def __init__(self, id_rain_prob: str, desc_rain_prob: str, id_rain_intensity: str, desc_rain_intensity: str):
        self.id_rain_prb = id_rain_prob
        self.desc_rain_prob = desc_rain_prob
        self.id_rain_intensity = id_rain_intensity
        self.desc_rain_intensity = desc_rain_intensity

class Temperature:

    def __init__(self, id_temp_prob: str, desc_temp_prob: str):
        self.id_temp_prob = id_temp_prob
        self.desc_temp_prob = desc_temp_prob

class Wind:

    def __init__(self, id_alt: str, desc_alt: str, id_dir_alt: str, desc_dir_alt: str, id_val: str, desc_val: str,
                 id_dir_val: str, desc_dir_val: str, icon_alt: str):
        self.id_alt = id_alt
        self.desc_alt = desc_alt
        self.id_dir_alt = id_dir_alt
        self.desc_dir_alt = desc_dir_alt
        self.id_val = id_val
        self.desc_val = desc_val
        self.id_dir_val = id_dir_val
        self.desc_dir_val = desc_dir_val
        self.icon_alt = icon_alt

class Range:

    def __init__(self, id_range: int, id_pred_range: int, range: str, range_name: str, range_time: str, icon: Icon, rain: Rain, temp: Temperature,  wind: Wind, zero: int, snow_lim: int):
        self.id_range = id_range
        self.id_pred_range = id_pred_range
        self.range = range
        self.range_name = range_name
        self.range_time = range_time
        self.icon = icon
        self.rain = rain
        self.temp = temp
        self.wind = wind
        self.zero = zero
        self.snow_lim = snow_lim

class Day:

    def __init__(self, id: int, id_pred_day: int, day: str, icon: Icon, desc_day: str, tmin: float, tmax: float, ranges: List[Range]):
        self.id = id
        self.id_pred_day = id_pred_day
        self.day = day
        self.icon = icon
        self.desc_day = desc_day
        self.tmin = tmin
        self.tmax = tmax
        self.ranges = ranges

class Prediction:

    def __init__(self, id_locality: int, locality: str, days: List[Day]):
        self.id_locality = id_locality
        self.id_locality = locality
        self.days = days

class TotPrediction:

    def __init__(self, id_prediction: int, date: str, evolution: str, short_evolution: str, predictions: List[Prediction]):
        self.id_prediction = id_prediction
        self.date = date
        self.evolution = evolution
        self.short_evolution = short_evolution
        self.predictions = predictions