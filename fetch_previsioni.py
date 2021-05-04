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
                '''print(type(pred['giorni']))
                print(pred['giorni'])'''
                for giorno in pred['giorni']:
                    #print(type(pred['giorni']))
                    for fascia in giorno['fasce']:
                        el = {}
                        el['localita'] = pred['localita'].lower()
                        #print(el['localita'])
                        el['data'] = datetime.strptime(giorno['giorno'], '%Y-%m-%d').date()
                        el['id_previsione_giorno'] = pred['giorni'].index(giorno)#['giorno']#['idPrevisioneGiorno']
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
        #for i in final_predictions_list:
        #print(Previsione.to_repr(i))
        return final_predictions_list


def get_both(prediction_json: dict, list_stations):
    stations_both = []
    for pred in prediction_json['previsione']:  # prediction_json['previsione'] -> type = list

        if pred['localita'].lower() in list_stations:
            stations_both.append(pred['localita'].lower())

    return(stations_both)




if __name__ == "__main__":

    fetch_previsioni = FetchPrevisioni()

    #previsioni_manager = MysqlPrevisioniManager()

    pred = fetch_previsioni.fetch_prediction("https://www.meteotrentino.it/protcivtn-meteo/api/front/previsioneOpenDataLocalita?localita")

    file = open("pickle/file_name1.pickle", 'rb')
    list_station_name = pickle.load(file)
    prev_no_stations = fetch_previsioni.remove_not_station(pred, list_station_name)
    #both = get_both(pred, list_station_name)

    f = open("guru99.txt", "w+")
    for i in range(10):
        f.write("This is line %d\r\n" % (i + 1))
        print("ciao ciao ciao")
    f.close()
    
    #print(prev_no_stations)
    '''for i in prev_no_stations:
        print(Previsione.to_repr(i))'''
    #previsioni_manager.save(prev_no_stations)

    '''print("ciao")
    f = open("guru99.txt", "w+")
    for i in range(10):
        f.write("This is line %d\r\n" % (i + 1))
        print("ciao ciao ciao")
    f.close()'''


'''zip_both = []
    for i in stat_code:
        if i[1] in both:
            zip_both.append(i)
        else:
            print(i)
    print(len(stat_code))
    print(len(zip_both))
    print(len(list_station_name))
    print(zip_both)
    file = open('pickle/both_zip_stations_codes.pickle',
                'wb')  # no duplicates of names od stations (since we consider different zones of same station)
    pickle.dump(zip_both, file)

    file = open('pickle/both_zip_stations_codes.pickle',
                'rb')  # no duplicates of names od stations (since we consider different zones of same station)
    x = pickle.load(file)
    print(x)'''