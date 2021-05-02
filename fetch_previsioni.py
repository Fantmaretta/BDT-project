import requests
from datetime import datetime
import pickle
import time
from prediction import Previsione, MysqlPrevisioniManager



class FetchPrevisioni:

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

        :param prediction_json:
        :param list_stations: pickle list of stations names
        :return:
        '''
        list_predictions = []
        for pred in prediction_json['previsione']: # prediction_json['previsione'] -> type = list

            if pred['localita'].lower() in list_stations:
                for giorno in pred['giorni']:
                    for fascia in giorno['fasce']:
                        el = {}
                        el['localita'] = pred['localita'].lower()
                        #print(el['localita'])
                        el['data'] = datetime.strptime(giorno['giorno'], '%Y-%m-%d').date()
                        el['id_previsione_giorno'] = giorno['idPrevisioneGiorno']
                        el['temp_min'] = giorno['tMinGiorno'] # on all day
                        el['temp_max'] = giorno['tMaxGiorno'] # on all day
                        el['fascia'] = fascia['fasciaOre']
                        # info below here are referred to the single fascia
                        el['id_prec_prob'] = fascia['idPrecProb']
                        el['desc_prec_prob'] = fascia['descPrecProb']
                        el['id_prec_int'] = fascia['idPrecInten']
                        el['desc_prec_int'] = fascia['descPrecInten']
                        el['id_alt'] = fascia['idVentoIntQuota']
                        el['desc_alt'] = fascia['descVentoIntQuota']
                        el['id_dir_alt'] = fascia['idVentoDirQuota']
                        el['desc_dir_alt'] = fascia['descVentoDirQuota']
                        el['id_val'] = fascia['idVentoIntValle']
                        el['desc_val'] = fascia['descVentoIntValle']
                        el['id_dir_val'] = fascia['idVentoDirValle']
                        el['desc_dir_val'] = fascia['descVentoDirValle']

                        #print(pred['localita'].lower())
                        #print(prediction_json['previsione'][])
                        #print(el)
                        list_predictions.append(el)
                        #print(list_predictions)
                #prediction_json['previsione'].remove(pred)
                #del pred
        #print(list_predictions)
        final_predictions_list = [Previsione.from_repr(raw_pred) for raw_pred in list_predictions]

        return final_predictions_list #list_predictions


if __name__ == "__main__":

    fetch_previsioni = FetchPrevisioni()

    #previsioni_manager = MysqlPrevisioniManager()

    pred = fetch_previsioni.fetch_prediction("https://www.meteotrentino.it/protcivtn-meteo/api/front/previsioneOpenDataLocalita?localita")

    file = open("/home/veror/PycharmProjects/BDT project/pickle/file_name1.pickle", 'rb')
    list_station_name = pickle.load(file)
    prev_no_stations = y = fetch_previsioni.remove_not_station(pred, list_station_name)

    print(prev_no_stations)

    #previsioni_manager.save(prev_no_stations)