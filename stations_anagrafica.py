import requests
import xml.etree.cElementTree as ET
import pickle
import re

class StationAnagrafica:
    
    def get_station_anagrafica(self, url_stations_anagrafica, file_station_name):
        '''
        given the url with stations information and the name of the file that will contain stations names, it extracts
        stations codes, names and short names and saves them into pickle files
        :param url_stations_anagrafica:
        :param file_station_name:
        :return:
        '''

        # file_station_name = 'stations.xml'

        # url stations anagrafica
        #url_stations_anagrafica = "http://dati.meteotrentino.it/service.asmx/listaStazioni"

        # request get
        resp_stat = requests.get(url_stations_anagrafica)

        # create xml file
        with open(file_station_name, 'wb') as f:
            f.write(resp_stat.content)

        # create tree
        tree = ET.parse(file_station_name)

        # get root element
        root = tree.getroot()

        # initialize interesting lists -> code, name, short name of all the stations
        codes = []
        names = []
        short_names = []

        # get all the codes
        for code in root.findall('.//{http://www.meteotrentino.it/}codice'):
            codes.append(code.text)
        codes.remove('T0396')
        # get all the names
        for name in root.findall('.//{http://www.meteotrentino.it/}nome'):
            # remove part of the name in parenthesis
            modified_name = re.sub(r" \([^()]*\)", "", name.text)
            names.append(modified_name.lower())
        names.remove('sarca di val genova al ghiacciaio del mandrone')
        zip_codes_names = (list(zip(codes, names)))
        # remove duplicates
        set_modified_name = set(names)
        names = list(set_modified_name)
        # get all the short names
        for short_name in root.findall('.//{http://www.meteotrentino.it/}nomebreve'):
            short_names.append(short_name.text)


        # save lists into pickles
        file_code = open('pickle/file_code1.pickle', 'wb')
        pickle.dump(codes, file_code)
        file_name = open('pickle/file_name1.pickle', 'wb') # no duplicates of names od stations (since we consider different zones of same station)
        pickle.dump(names, file_name)
        file_short_name = open('pickle/file_short_name1.pickle', 'wb')
        pickle.dump(short_names, file_short_name)
        file_zip_code_name = open('pickle/file_zip_code_name1.pickle', 'wb')
        pickle.dump(zip_codes_names, file_zip_code_name)


if __name__ == "__main__":
    station_anagrafica = StationAnagrafica()
    station_anagrafica.get_station_anagrafica("http://dati.meteotrentino.it/service.asmx/listaStazioni", 'stations.xml')
