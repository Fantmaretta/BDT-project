import pandas as pd
import numpy as np
import requests
import xml.etree.cElementTree as ET
from xml.parsers import expat
from lxml import etree
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
        #print(resp_stat.content)

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

        '''print(codes)
        print(names)
        print(short_names)'''



# questo da spostere nel main
station_anagrafica = StationAnagrafica()
station_anagrafica.get_station_anagrafica("http://dati.meteotrentino.it/service.asmx/listaStazioni", 'stations.xml')



















'''xmlstr = ET.tostring(root, encoding='utf8', method='xml')

root = fromstring(xmlstr)
for actor in root.findall('{http://people.example.com}actor'):
    name = actor.find('{http://people.example.com}name')
    print(name.text)
    for char in actor.findall('{http://characters.example.com}character'):
        print(' |-->', char.text)'''





'''inputfile = 'file.xml'
target_ns = '{http://www.meteotrentino.it/}'
nsmap = {None: target_ns}

tree = etree.parse(inputfile)
root = tree.getroot()
'''
# here we set the namespace of all elements to target_ns
'''for elem in root.getiterator():
    tag = etree.QName(elem.tag)
    elem.tag = '{%s}%s' % (target_ns, tag.localname)

# create a new root element and set the namespace map, then
# copy over all the child elements
new_root = etree.Element(root.tag, nsmap=nsmap)
new_root[:] = root[:]

# create a new elementtree with new_root so that we can use the
# .write method.
tree = etree.ElementTree()
tree._setroot(new_root)

tree.write('done.xml',
           pretty_print=True, xml_declaration=True, encoding='UTF-8')'''

'''print(root.tag)
for x in root.findall('{http://www.meteotrentino.it/}ArrayOfAnagrafica'):
    code = x.find('{http://www.meteotrentino.it/}codice')
    print(code.text)'''
'''for child in root.iter():
    from r in document.Descendants(ns + "Credential")
    select(string)
    r.Element(target_ns + "Username");
    print(child)
    #print(child.tag, child.attrib)
    print(child.tag, child.attrib[target_ns + 'codice'])'''



'''
# Remove namespace prefixes
for elem in root.getiterator():
    elem.tag = etree.QName(elem).localname
# Remove unused namespace declarations
etree.cleanup_namespaces(root)

print(etree.tostring(root).decode())

url_stations_anagrafica = "http://dati.meteotrentino.it/service.asmx/listaStazioni"
resp_stat = requests.get(url_stations_anagrafica)
#print(resp_stat.content)

with open('stations.xml', 'wb') as f:
    f.write(resp_stat.content)

class DisableXmlNamespaces:
    def __enter__(self):
            self.oldcreate = expat.ParserCreate
            expat.ParserCreate = lambda encoding, sep: self.oldcreate(encoding, None)
    def __exit__(self, type, value, traceback):
            expat.ParserCreate = self.oldcreate

def parseXML(xmlfile):
    # create element tree object
    with DisableXmlNamespaces():
        tree = ET.parse("file.xml")

    # get root element
    root = tree.getroot()

    print(root.findall('{http://www.meteotrentino.it/}codice'))
    # create empty list for news items
    newsitems = []

    for child in root.iter():
        print(child)
        #print(child.tag, child.attrib)
        #print(child.tag, child.attrib['codice'])

parseXML('stations.xml')

root = ET.fromstring(resp_stat.content)

for child in root.iter('*'):
    print(child.tag, child.attrib['codice'])

#root = tree.getroot()
#tree = ET.ElementTree(root)
#tree.write("file.xml")
#print(root.text)


for code in root.iter("ns0:codice"):
    print(code)
    codes.append(code.text)

print(codes)
'''


