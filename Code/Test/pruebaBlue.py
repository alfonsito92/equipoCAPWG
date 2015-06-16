import bluetooth

def discoverNearBluetoothDevices():
    nearby_devices = bluetooth.discover_devices()    #Escanea los dispositivos bluetooth cercanos
    return nearby_devices

target_name = ""
target_address = None
nearby_devices=discoverNearBluetoothDevices()
print ("algo " +str(nearby_devices))

for bdaddr in nearby_devices:
    target_name == bluetooth.lookup_name( bdaddr )
    target_address = bdaddr
    print "Found bluetooth device with name "+target_name+" and address "+target_address
