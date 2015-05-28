import time
import bluetooth

def pruebaTiempo():
    result = bluetooth.lookup_name('4C:74:03:1D:87:69', timeout=0.8)
    if(result != None):
        print "Esta cerca"
    else:
        print "No lo esta"

try:
    pruebaTiempo()

except KeyboardInterrupt:
    print "Se cierra"
