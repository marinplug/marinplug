import machine
try:
    import usocket as socket
except:
    import socket
  
from time import sleep
import network, urequests

# Les lignes suivantes désactivent les messages de débogage du système d'exploitation 
import esp
esp.osdebug(None)

# Economiser de l'espace dans la mémoire flash.  (Clear)
import gc
gc.collect()

#-----------------------------------------------
#-- VARIABLES PRIVATE
from unit.GLB import ESP_IP, ESP_MASQ, ESP_DNS, ESP_GATEWAY
from unit import ota_repo, secret, GLB

 # enable station interface and connect to Wi-Fi station
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(secret.WLAN_SSID, secret.WLAN_PASSWORD)

while station.isconnected() == False:
    pass
 
GLB.printDEB('Connection successful')
#-- WLAN.ifconfig([(ip, subnet, gateway, dns)])
ESP_IP, ESP_MASQ, ESP_GATEWAY, ESP_DNS=station.ifconfig()
GLB.printDEB( 'Adresses:{}-{}-{}'.format(ESP_IP, ESP_MASQ, ESP_GATEWAY) )


#-------------------------------------------------
#-- Request risque d'dexception
#-- 
try:
    objOTA=ota_repo.CLOta_files(
        url='http://ota_server.com:8085'   # Required
    )
    GLB.printDEB("--- URL OTA:{}".format(objOTA.url) )
    GLB.printDEB("--- FILES OTA:{}".format(objOTA.files))

    ##print( "Check if newer version is available.:{}".format( objOTA.fetch() ))
    if objOTA.update():
        GLB.printDEB("--- UPDATED OTA to the latest version! Rebooting...")
        machine.reset()
except Exception as ex:
    GLB.printDEB("Exception ERROR:{}".format(ex) )
    