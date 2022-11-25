try:
    import usocket as socket
except:
    import socket
  
from time import sleep
import network
import gc
import ure
from unit import GLB
from stations import stations_xml

#-----------------------------------------------
#-- VARIABLES PRIVATE
version = "1.1.0" # Version avec OTA

#-----------------------------------------------
#-- FUNCTIONS
def sendOK(client):
    payload = "<h2>ESP MicroPython Web Server HELLO</h2>"
    send_response(client, payload)
def sendERROR(client):
    payload = "<h2>ESP MicroPython Web Server ERROR REQUEST</h2>"
    send_response(client, payload)

def sendXML(client, contentXML ):
    xml_data = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
    xml_data += contentXML
    #xml_data= '<h2>{}</h2>'.format(xml_data)
    send_response( client, xml_data)

#-----------------------------------------------
#-- send_response
#-- payload='' ou webpage
def send_response(client, payload, status_code=200):
    content_length = len(payload)
    send_header(client, status_code, content_length)
    if content_length > 0:
        client.sendall(payload)
    client.close()

#-----------------------------------------------
#-- send_header
def send_header(client, status_code=200, content_length=None ):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
      client.sendall("Content-Length: {}\r\n".format(content_length))
    client.sendall("\r\n")

#-----------------------------------------------
#-- routeReqHTTP: Fonction qui dispatch les commandes
#-- RETOUR BOOL
def routeReqHTTP(client, request):
    dtReq=GLB.getDtRequest(request)
    GLB.printDEB("routeReqHTTP: dtReq={}".format(dtReq))
    reqValide=GLB.len(dtReq)>0
    if( not reqValide ): return reqValide
    pathURL= dtReq[GLB.CT_PATHURL]
    try:
        # ETAPE 1: Mise sous tension du YAHAMA CD301N
        if( 'token' in dtReq[GLB.CT_VARS] ):
            sendXML(client,'<EncryptedToken>0000000000000000</EncryptedToken>') 
        
        # ETAPE 2: Admin (sans objet)
        elif(  pathURL.startswith('/admin/') ):
            reqValide=False
        
        # ETAPE 3: Initialise liste radios (max 10 radios)
        elif( pathURL.startswith('/setupapp/') ):
            sendXML(client, stations_xml.xmlRadios() )

        # ETAPE 4: Initialise liste staions de la radio (max 10 stations)
        elif(  pathURL.startswith('/ycast/') ):
            nameRadio= pathURL[7:]
            sendXML(client, stations_xml.xmlRadioStations( nameRadio ) )
        else:
            reqValide=False
    finally:
        pass
          
    return reqValide

#-----------------------------------------------
#-- MAIN après connexion WIFI établie dans boot.py
# CREER une sockect, port 1080, max 1 écoute
print( "main version={}".format(version))

#-- INITIALISER sniffeur YAMAHA port 80 pour ycasr
port=80
addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
print('socket.getaddrinfo ={}'.format(addr))
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(addr)
server_socket.listen(1)

reqValide=False
while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        client, addr = server_socket.accept()
        print('\nReceived HTTP GET from %s' % str(addr))

        #-- LIRE le paquet entier de bytes émis
        client.settimeout(5.0)
        data = b""
        try:
            while "\r\n\r\n" not in data:
                data += client.recv(512)
        except OSError:
            pass
        client.settimeout(None)
        
        # conversion en str
        request = data.decode('utf-8')
        GLB.printDEB('Content = %s' % request)

        #-- VERIFIER request HTTP valide
        reqValide=(len(request)>10 and request.index(' HTTP/', 10)  )
        if( reqValide ):
            reqValide= routeReqHTTP(client, request)

    finally:
        if(not reqValide):
            sendERROR(client)
        client.close()
