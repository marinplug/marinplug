import builtins
import re

#-----------------------------------------------
#-- VARIABLE GLOBALES

ESP_IP='0.0.0.0'
ESP_MASQ='0.0.0.0'
ESP_GATEWAY='0.0.0.0'
ESP_DNS='0.0.0.0'

#-----------------------------------------------
#-- FONCTIONS STATIQUES
#-----------------------------------------------

#-----------------------------------------------
#-- printConsole
DEBUG=True
def printDEB(msg):
    if(DEBUG):
        print(msg)

#-----------------------------------------------
#-- countList: remplace len(list) pas OK!!!
def countList(lst):
    count=0
    for a in lst:
        count+=1
    return count

#-----------------------------------------------
#-- import builtins--> count=builtins.len(lst) OK!!!
def len( obj ):
    return builtins.len(obj)

#-----------------------------------------------
#-- re_split remplace re.slpit
#-- "[\r\n]" pour ligne
#-- r"[ ?=&]+" separateurs: ' ', '?', '=', '&' + multi recherches, pour liste variables
def re_split( filter, ch ):
    regex = re.compile(filter)
    return regex.split( ch )

#-----------------------------------------------
#-- getDtRequest
#-- chR= 'GET /setupapp/Yamaha/asp/BrowseXML/loginXML.asp?token=0 HTTP/1.1 ... Requests: 1\r\nSec-GPC: 1\r\n\r\n'
#-- RETURN dict 
CT_METHODE = 'method'
CT_PATHURL = 'pathURL'
CT_VARS = 'vars'
CT_PROTO = 'proto'
def getDtRequest( chR ):
    req={}
    try:
        reqLines = re_split( "[\r\n]", chR )
        chSplit = re_split( r"[ ?=&]+", reqLines[0] )
        count = len( chSplit )
        req={}
        req[CT_METHODE] = chSplit[0]
        req[CT_PATHURL] = chSplit[1]
        dt={}
        for i in range(2, count-1, 2):
            dt[chSplit[i]]=chSplit[i+1]
        req[CT_VARS]=dt
        req[CT_PROTO]=chSplit[count-1]
    finally:
        pass
    return req
