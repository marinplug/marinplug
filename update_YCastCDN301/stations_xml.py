import re
from collections import OrderedDict
from unit import GLB
#-----------------------------------------------
#-- VARIABLE GLOBALES
dtRadios = None 

#-----------------------------------------------
#-- appendDictItem: Ajout une clé et valeur au dictionnire
def appendDictItem( dt, key, value ):
    # replace multiple spaces with a single space
    key= re.sub(' +', ' ', key)
    dt[key]=value

def xmlRadios():
    return _xmlRadios( dtRadios )
def _xmlRadios(dt):
    xml='<ListOfItems>'
    for key in dt.keys():
        xml+='<Item>'
        xml+='<ItemType>Dir</ItemType>'
        xml+='<Title>{}</Title>'.format(key)

        key = re.sub(' ', '%20', key ) # remplacer espace par %20
        xml+='<UrlDir>http://radioyamaha.vtuner.com/ycast/{}</UrlDir>'.format( key )
        xml+='</Item>'
    xml+='</ListOfItems>'
    return xml

def xmlRadioStations( nameRadion ):
    name = re.sub( '%20', ' ',  nameRadion ) # remplacer  %20 par espace 
    return xmlRadioItems( dtRadios[ name ] )
def xmlRadioItems(dt):
    xml='<ListOfItems>'
    for key, value in dt.items():
        xml+='<Item>'
        xml+='<ItemType>Station</ItemType>'
        xml+='<StationName>{}</StationName>'.format(key)
        xml+='<StationUrl>{}</StationUrl>'.format(value)
        xml+='</Item>'
    xml+='</ListOfItems>'
    return xml

def getStationsFrom( dtRadios, nameRadio ):
    xml=''
    key = re.sub( '%20', ' ', nameRadio ) # remplacer %20 par espace
    xml = xmlRadioItems( dtRadios[key] )
    return xml

#-----------------------------------------------
#-- conv_yml_dt: Convertir un fichier yml en json
#-- arg: nom du fichier 'stations.yml'
#-- retour: dict Radio
def conv_yml_dt( fileyml ):
    # ouvrir fichier 'conv_yml_xml'
    file = open( fileyml, "r")
    lines=file.readlines()
    file.close()

    global dtRadios
    dtRadios= OrderedDict() #{} Pour avoir des dict ordonnées selon l'ajout des items
    dt = None
    nameRadio=None
    count = 0
    # Strips the newline character
    for line in lines:
        count += 1
        line=line.strip()
        if(len(line)>2):
            lastcar = line[-1]
            if(lastcar == ':'):		# UNE nouvelle RADIO
                if( nameRadio!=None ):	
                    # Ajouter stations à la radio précédente
                    appendDictItem(dtRadios,  nameRadio, dt)
                dt=OrderedDict()
                nameRadio=line[:-1]
            elif( dt!=None ):             # SI RADIO Valide ajouter nouvelle station
                id=line.index(':')
                key=line[:id]
                value=line[id+1:]
                appendDictItem(dt,  key, value)

    GLB.printDEB("Liste stations:\n{}".format(dtRadios))
#-----------------------------------------
#-- START avec le premier import 
#-- INITIALISER Dict radios
conv_yml_dt('stations.yml')