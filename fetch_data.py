import requests
from typing import List

import pickle

class Fetch:

    def fetch_prediction(self, url_prediction: str):
        '''

        :param url_prediction:
        :return:
        '''
        #url_prediction = "https://www.meteotrentino.it/protcivtn-meteo/api/front/previsioneOpenDataLocalita?localita"
        resp_pred = requests.get(url_prediction)
        prediction = resp_pred.json()
        #print(prediction)
        return prediction

    def remove_not_station(self, prediction_json: dict, list_stations):
        '''

        :param prediction_json:
        :return:
        '''
        for pred in prediction_json['previsione']:
            #print(pred)
            if pred['localita'].lower() not in list_stations:
                print(pred['localita'].lower())
                print(prediction_json['previsione'][pred])
                del prediction_json['previsione'][pred]

    def fetch_data(self, url_data: str, list_station_code: List[str]):
        '''

        :param url_data:
        :param list_station_code:
        :return:
        '''
        list_resp_data = [requests.get(url_data + station_id) for station_id in list_station_code]
        return list_resp_data

        '''for i in list_resp_data:
            print(i.content)'''
        '''url_data = "http://dati.meteotrentino.it/service.asmx/ultimiDatiStazione?codice=T0153"
        resp_data = requests.get(url_data)
        print(resp_data.content)'''

# da mettere nel main
fetch = Fetch()

file = open("/home/veror/PycharmProjects/BDT project/pickle/file_name.pickle",'rb')
list_station_name = pickle.load(file)
x = fetch.fetch_prediction("https://www.meteotrentino.it/protcivtn-meteo/api/front/previsioneOpenDataLocalita?localita")
print(fetch.remove_not_station(x, list_station_name))

'''file = open("/home/veror/PycharmProjects/BDT project/pickle/file_code.pickle",'rb')
list_station_code = pickle.load(file)
print(list_station_code)
fetch.fetch_data("http://dati.meteotrentino.it/service.asmx/ultimiDatiStazione?codice=T0153", list_station_code)
'''
#data = resp_data.xml()

#print(stations)

#print(prediction["previsione"][0])