import requests
from typing import List
import pickle
import xml.etree.cElementTree as ET
from datetime import datetime, timedelta
from dati_reali import DatiReali, MySQLDatiRealiManager
import time


def create_times_day():
    spacing = 15    # in minutes
    lst = [(datetime.strptime(str(i * timedelta(minutes=spacing)), '%H:%M:%S')).time() for i in range(24 * 60 // spacing)]
    #print(lst)
    return lst


class FetchDati:


    def fetch_single_station(self, url_data: str, station_code_name: (str, str)):

        resp_data = requests.get(url_data + station_code_name[0])

        root = ET.fromstring(resp_data.content)

        '''for child in root.iter('*'):
            print(child.tag)'''

        if root.find('.//{http://www.meteotrentino.it/}data').text is not None:
            data_oggi = (datetime.strptime(root.find('.//{http://www.meteotrentino.it/}data').text, '%Y/%m/%d')).date()
        else:
            data_oggi = None
        if root.find('.//{http://www.meteotrentino.it/}tmin').text is not None:
            temp_min = float(root.find('.//{http://www.meteotrentino.it/}tmin').text)
        else:
            temp_min = None
        if root.find('.//{http://www.meteotrentino.it/}tmax').text is not None:
            temp_max = float(root.find('.//{http://www.meteotrentino.it/}tmax').text)
        else:
            temp_max = None
        if root.find('.//{http://www.meteotrentino.it/}rain').text is not None:
            rain = float(root.find('.//{http://www.meteotrentino.it/}rain').text)
        else:
            rain = None

        # TODO NON SI CAPISCE COME USARE TMAX E TMIN, NON CORRISPONDONO ALLE OSSERVAZIONI RIPORTATE SOTTO, MAGARI
        # TODO POSSIAMO NON USARLE E RICAVARCELE DAI DATI

        date_ore_t = []
        temperature = []
        for temperatura_aria in root.findall('.//{http://www.meteotrentino.it/}temperatura_aria'):
            for data_ora in temperatura_aria.findall('.//{http://www.meteotrentino.it/}data'):
                if data_ora is not None:
                    data, ora = (datetime.fromisoformat(data_ora.text)).date(), (datetime.fromisoformat(data_ora.text)).time()
                    date_ore_t.append((data, ora))
                else:
                    date_ore_t.append(None)
            for temperatura in temperatura_aria.findall('.//{http://www.meteotrentino.it/}temperatura'):
                if temperatura is not None:
                    temperature.append(float(temperatura.text))
                else:
                    temperature.append(None)
        data_ora_temp = list(zip(date_ore_t, temperature))
        #print('1', data_ora_temp)
        #print(len(data_ora_temp))

        date_ore_p = []
        piogge = []
        for precipitazione in root.findall('.//{http://www.meteotrentino.it/}precipitazione'):
            for data_ora in precipitazione.findall('.//{http://www.meteotrentino.it/}data'):
                if data_ora is not None:
                    data, ora = (datetime.fromisoformat(data_ora.text)).date(), (
                        datetime.fromisoformat(data_ora.text)).time()
                    date_ore_p.append((data, ora))
                else:
                    date_ore_p.append(None)
            for pioggia in precipitazione.findall('.//{http://www.meteotrentino.it/}pioggia'):
                if pioggia is not None:
                    piogge.append(float(pioggia.text))
                else:
                    piogge.append(None)
        data_ora_prec = list(zip(date_ore_p, piogge))
        #print('1', data_ora_prec)
        #print(len(data_ora_prec))

        date_ore_v = []
        venti_vel = []
        venti_dir = []
        for vento in root.findall('.//{http://www.meteotrentino.it/}vento_al_suolo'):
            for data_ora in vento.findall('.//{http://www.meteotrentino.it/}data'):
                if data_ora is not None:
                    data, ora = (datetime.fromisoformat(data_ora.text)).date(), (datetime.fromisoformat(data_ora.text)).time()
                    date_ore_v.append((data, ora))
                else:
                    date_ore_v.append((None, None))
            for velocita in vento.findall('.//{http://www.meteotrentino.it/}v'):
                if velocita is not None:
                    venti_vel.append(float(velocita.text))
                else:
                    venti_vel.append(None)
            for direzione in vento.findall('.//{http://www.meteotrentino.it/}d'):
                if direzione is not None:
                    venti_dir.append(float(direzione.text))
                else:
                    venti_dir.append(None)
        data_ora_v_d = list(zip(date_ore_v, venti_vel, venti_dir))
        #print('3', data_ora_v_d)
        #print(len(data_ora_v_d))

        #print('4', list(zip(data_ora_temp, data_ora_v_d, data_ora_prec)))
        #print(len(list(zip(data_ora_temp, data_ora_v_d, data_ora_prec))))

        #print({'localita': station_code_name[1], 'data_oggi': data_oggi, 'temp_min': temp_min, 'temp_max': temp_max, 'rain': rain, 'data_ora_temp': data_ora_temp, 'data_ora_prec': data_ora_prec, 'data_ora_v_d': data_ora_v_d})


        #print("-----------------------------------------------------------------\n")

        # NB PU0' ESSERE CHE NON FACCIA ESATTAMENTE OGNI QUARTO D'ORA !!!!!!!!!!!!!!!
        # IN PARTICOLARE NEI VENTI, GLI ALTRI DUE INVECE SEMBRANO ESSERE SEMPRE CORRETTI
        # MA OK TANTO NOI FACCIAMO UNA MEDIA
        # in alcuni posti possono non esserci delle osservazioni -> eg: borgo valsugana non ha i venti

        return {'station_code': station_code_name[0], 'localita': station_code_name[1], 'data_oggi': data_oggi, 'temp_min': temp_min, 'temp_max': temp_max, 'rain': rain, 'data_ora_temp': data_ora_temp, 'data_ora_prec': data_ora_prec, 'data_ora_v_d': data_ora_v_d}


    def fetch_data(self, url_data: str, list_station_code_name: List[tuple]):
        '''
        Given an url and one list containing stations' codes, it returns the actual meteorological data from that url
        only for the stations with those codes (localities that are meteorological stations)
        :param url_data:
        :param list_station_code:
        :return:
        '''

        list_resp_data = []
        ''' for station_code_name in list_station_code_name:
            try:
                list_resp_data.append(self.fetch_single_station(url_data, station_code_name))
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue'''
        for station_code_name in list_station_code_name:
            list_resp_data.append(self.fetch_single_station(url_data, station_code_name))
            time.sleep(2)
        #list_resp_data = [self.fetch_single_station(url_data, station_code_name) for station_code_name in list_station_code_name]

        return list_resp_data


    def from_fetch_to_repr_station(self, dict_data, list_time):

        records = {}
        for time in list_time:
            data = dict_data['data_oggi'] - timedelta(days=1)
            records[(data, time)] = {'station_code': dict_data['station_code'], 'localita': dict_data['localita'], 'data': data, 'time': time, 'temperatura': None, 'pioggia': None, 'vento_velocita': None, 'vento_direzione': None}

        for t in dict_data['data_ora_temp']:
            data_t = t[0][0]
            ora_t = t[0][1]
            temp = t[1]
            if (data_t, ora_t) in records:
                records[(data_t, ora_t)]['temperatura'] = temp

        for p in dict_data['data_ora_prec']:
            data_p = p[0][0]
            ora_p = p[0][1]
            prec = p[1]
            if (data_p, ora_p) in records:
                records[(data_p, ora_p)]['pioggia'] = prec

        for v in dict_data['data_ora_v_d']:
            data_v = v[0][0]
            ora_v = v[0][1]
            vel_v = v[1]
            dir_v = v[2]
            if (data_v, ora_v) in records:
                records[(data_v, ora_v)]['vento_velocita'] = vel_v
                records[(data_v, ora_v)]['vento_direzione'] = dir_v

        records_list = []
        for key in records:
            record_single = DatiReali.from_repr(records[key])
            records_list.append(record_single)

        return(records_list)


    def from_fetch_to_repr_tot_stations(self, output_fetch_data, list_time):
        return [self.from_fetch_to_repr_station(out, list_time) for out in output_fetch_data]


if __name__ == "__main__":

    fetch_dati = FetchDati()

    dati_manager = MySQLDatiRealiManager()

    file1 = open("/home/veror/PycharmProjects/BDT project/pickle/both_zip_stations_codes.pickle", 'rb')
    list_station_codes_names = pickle.load(file1)
    '''file2 = open("/home/veror/PycharmProjects/BDT project/pickle/file_zip_code_name1.pickle", 'rb')
    list_station_codes_names = pickle.load(file2)'''

    list_time = create_times_day()

    dati = fetch_dati.fetch_data(' http://dati.meteotrentino.it/service.asmx/ultimiDatiStazione?codice=',
                         list_station_codes_names)

    tot_dati = fetch_dati.from_fetch_to_repr_tot_stations(dati, list_time)

    #print(tot_dati)

    dati_manager.save(tot_dati)






























# da mettere nel main
#fetch = FetchDati()

#TODO CODICE PER RUNNARE FETCH DATI REALI
'''file = open("/home/veror/PycharmProjects/BDT project/pickle/prova.pickle",'rb')
y = pickle.load(file)'''
#y = fetch.fetch_data(' http://dati.meteotrentino.it/service.asmx/ultimiDatiStazione?codice=', list_station_codes_names)
'''file_name = open('pickle/prova.pickle', 'wb') # no duplicates of names od stations (since we consider different zones of same station)
pickle.dump(y, file_name)'''
'''y2 = fetch.from_fetch_to_repr_tot_stations(y, list_time)


for i in y2:
    for j in i:
        print(j)

print(y2)'''
#print(y2)













'''file_name = open('pickle/prova3.pickle', 'wb') # no duplicates of names od stations (since we consider different zones of same station)
pickle.dump(y2, file_name)'''

'''file2 = open("/home/veror/PycharmProjects/BDT project/pickle/prova2.pickle",'rb')
res = pickle.load(file2)

for x in res:
    print(x)'''


'''def fetch_all(self, url_pred, url_data, list_station_code):
   
    # fetch predictions
    schedule.every(5).seconds.do(self.fetch_prediction, url_pred)
    schedule.every().hour.do(self.fetch_prediction, url_pred)
    schedule.every().day.do(self.fetch_prediction, url_pred)
    # fetch data
    #schedule.every().hour.do(self.fetch_data, url_data, list_station_code)
    schedule.every().day.at("00:01").do(self.fetch_data, url_data, list_station_code)
    while True:
        schedule.run_pending()
        time.sleep(1)'''































'''x = fetch.fetch_single_station('http://dati.meteotrentino.it/service.asmx/ultimiDatiStazione?codice=', 'T0437')
print(x)'''

'''print(list_station_code)
print(len(list_station_code))
print(list_station_name)
print(len(list_station_name))
print(list_station_code_names)
print(len(list_station_code_names))'''

#print(list_station_code_names)







#file = open("/home/veror/PycharmProjects/BDT project/pickle/file_code.pickle",'rb')
#list_station_code = pickle.load(file)
#pred_e_data = fetch.fetch_all("https://www.meteotrentino.it/protcivtn-meteo/api/front/previsioneOpenDataLocalita?localita", "http://dati.meteotrentino.it/service.asmx/ultimiDatiStazione?codice=", list_station_code)

#x = fetch.fetch_data("http://dati.meteotrentino.it/service.asmx/ultimiDatiStazione?codice=", list_station_code)

#file = open("/home/veror/PycharmProjects/BDT project/pickle/file_name.pickle",'rb')
#list_station_name = pickle.load(file)
#y = fetch.fetch_prediction("https://www.meteotrentino.it/protcivtn-meteo/api/front/previsioneOpenDataLocalita?localita")
#y_new = fetch.remove_not_station(y, list_station_name)

'''for i in y_new:
    print(i , '\n')'''

'''print(len(y_new))
print(y_new)
print(list_station_name)
print(len(list_station_name))'''





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


# TODO CODICE PER FETCH PREVISIONI
#x = fetch.fetch_prediction("https://www.meteotrentino.it/protcivtn-meteo/api/front/previsioneOpenDataLocalita?localita")
#list_station_name.remove('daone')
'''for el in x:
    print(el)'''
#print(x)


'''file = open("/home/veror/PycharmProjects/BDT project/pickle/file_name1.pickle",'rb')
list_station_name = pickle.load(file)
#print(list_station_name)
y = fetch.remove_not_station(x, list_station_name)'''
'''for i in y:
    print(Previsione.to_repr(i))'''
'''
for i in y:
    print(i)
print(y)'''





#print(y)