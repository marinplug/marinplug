import machine
try:
    import usocket as socket
except:
    import socket
  
from time import sleep
import network

# Les lignes suivantes désactivent les messages de débogage du système d'exploitation 
import esp
esp.osdebug(None)

# Economiser de l'espace dans la mémoire flash.  (Clear)
import gc
gc.collect()

#-----------------------------------------------
#-- VARIABLES PRIVATE
from unit.GLB import ESP_IP, ESP_MASQ, ESP_DNS, ESP_GATEWAY
from unit import ota_repo, secret

 # enable station interface and connect to Wi-Fi station
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(secret.WLAN_SSID, secret.WLAN_PASSWORD)

while station.isconnected() == False:
    pass
 
print('Connection successful')
#-- WLAN.ifconfig([(ip, subnet, gateway, dns)])
ESP_IP, ESP_MASQ, ESP_GATEWAY, ESP_DNS=station.ifconfig()
print( 'Adresses:{}-{}-{}'.format(ESP_IP, ESP_MASQ, ESP_GATEWAY) )


#-------------------------------------------------
# PAS OK GITHUB_URL = "https://github.com/marinplug/marinplug/blob/main/"
# ERROR:  File "urequests.py", line 20, in content
##        MemoryError: memory allocation failed, allocating 94720 bytes
##--- URL Ok, pas d'erreur d'allocation de mémoire
GITHUB_URL = "https://raw.githubusercontent.com/marinplug/marinplug/main"
objOTA=ota_repo.CLOta_repo(
    user="marinplug",   # Required
    repo="marinplug",   # Required
    branch="main",      # Optional: Defaults to "master"
    working_dir=None,   # Optional: Defaults to None
    files = ["stations.yml"]
)
print("--- URL OTA:{}".format(objOTA.url) )
print("--- FILES OTA:{}".format(objOTA.files))
##print( "Check if newer version is available.:{}".format( objOTA.fetch() ))
if objOTA.update():
    print("--- UPDATED OTA to the latest version! Rebooting...")
    machine.reset()