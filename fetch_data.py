import requests
from typing import List
import pickle
import schedule
import time

class Fetch:

    def fetch_prediction(self, url_prediction: str):
        '''
        Given an url, it retrieves the data (json) from it (used for prediction data)
        :param url_prediction:
        :return:
        '''
        #url_prediction = "https://www.meteotrentino.it/protcivtn-meteo/api/front/previsioneOpenDataLocalita?localita"
        resp_pred = requests.get(url_prediction)
        prediction = resp_pred.json()
        return prediction

    def remove_not_station(self, prediction_json: dict, list_stations):
        '''
        It removes from the json the localities not matching a meteo station
        :param prediction_json:
        :return:
        '''
        list_localities = []
        for pred in prediction_json['previsione']: # prediction_json['previsione'] -> type = list
            if pred['localita'].lower() in list_stations:
                #print(pred['localita'].lower())
                #print(prediction_json['previsione'][])
                list_localities.append(pred)
                #prediction_json['previsione'].remove(pred)
                #del pred
        return list_localities

    def fetch_data(self, url_data: str, list_station_code: List[str]):
        '''
        Given an url and one list containing stations' codes, it returns the actual meteorological data from that url
        only for the stations with those codes (localities that are meteorological stations)
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


    # TODO decide time rate at which we want to do fetch
    def fetch_all(self, url_pred, url_data, list_station_code):
        '''
        It applies fetch functions for predictions and data every day, every hour
        :param url_pred:
        :param url_data:
        :param list_station_code:
        :return:
        '''
        # fetch predictions
        schedule.every(5).seconds.do(self.fetch_prediction, url_pred)
        schedule.every().hour.do(self.fetch_prediction, url_pred)
        schedule.every().day.do(self.fetch_prediction, url_pred)
        # fetch data
        schedule.every().hour.do(self.fetch_data, url_data, list_station_code)
        schedule.every().day.do(self.fetch_data, url_data, list_station_code)
        while True:
            schedule.run_pending()
            time.sleep(1)

# TODO connect DB -> relational? mysql

# da mettere nel main
fetch = Fetch()

file = open("/home/veror/PycharmProjects/BDT project/pickle/file_code.pickle",'rb')
list_station_code = pickle.load(file)
pred_e_data = fetch.fetch_all("https://www.meteotrentino.it/protcivtn-meteo/api/front/previsioneOpenDataLocalita?localita", "http://dati.meteotrentino.it/service.asmx/ultimiDatiStazione?codice=", list_station_code)


#print(fetch.fetch_all("https://www.meteotrentino.it/protcivtn-meteo/api/front/previsioneOpenDataLocalita?localita"))

# pickle file in which we have saved the names of the localities that are stations
'''file = open("/home/veror/PycharmProjects/BDT project/pickle/file_name.pickle",'rb')
list_station_name = pickle.load(file)
print(list_station_name)

# prediction
x = fetch.fetch_prediction("https://www.meteotrentino.it/protcivtn-meteo/api/front/previsioneOpenDataLocalita?localita")
#list_station_name.remove('daone')
print(x)
'''

# data
'''new = fetch.remove_not_station(x, list_station_name)
for pred in new:
    # print(pred)
    print(pred['localita'])'''


# print(list_station_code)
'''list_data = fetch.fetch_data("http://dati.meteotrentino.it/service.asmx/ultimiDatiStazione?codice=", list_station_code)
print(list_data)'''

#data = resp_data.xml()

#print(stations)

#print(prediction["previsione"][0])