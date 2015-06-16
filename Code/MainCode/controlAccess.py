import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep
import bluetooth
from BluezInquiry import BluezInquiry
import sys
from subprocess import Popen, PIPE

from __future__ import print_function
import mysql.connector
from mysql.connector.constants import ClientFlag

import sys
import time

GPIO.setmode(GPIO.BCM)   #Ponemos la Raspberry en modo BCM

dmin=40 #Distancia minima de los objetos a los sensores para iniciar un emparejamiento

servoPinBCM = 18

GPIO.setup(servoPinBCM,GPIO.OUT)
servo = GPIO.PWM(servoPinBCM,50)
servo.start(7.5)

posServoInicial = 6
posServo = 6
posServoSubido = 3
posServoBajado = 6

TRIGGER1 = 21
ECHO1 = 20

#TRIGGER2 = 24
#ECHO2= 23

pausa=5

#Funciones

##############SQL
#  Se crea la funcion que realiza la consulta
def run_query(query=''):

    config = {
	    'user': 'pcawg',
	    'password': '123456',
	    'host': '10.42.0.1',
	    'client_flags': [ClientFlag.SSL],
	    'ssl_ca': '/etc/mysql/ca.pem',
	    'ssl_cert': '/etc/mysql/client-cert.pem',
	    'ssl_key': '/etc/mysql/client-key.pem',
    }

    #datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME]

    #conn = MySQLdb.connect(*datos) # Conectar a la base de datos
    #cursor = conn.cursor()         # Crear un cursor
    #cursor.execute(query)          # Ejecutar una consulta

    conn = mysql.connector.connect(**config)	# Conectar a la base de datos
    cursor = conn.cursor(buffered=True) 	# Crear el cursor
    cursor.execute(query)			# Ejecutar una consulta

    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()   # Traer los resultados de un select
    else:
        conn.commit()              # Hacer efectiva la escritura de datos
        data = None

    cursor.close()                 # Cerrar el cursor
    conn.close()                   # Cerrar la conexion

    return data

def getDireccionesEntrar():
	aa = run_query("SELECT MAC FROM parking.Usuarios WHERE Acceso = 'SI' AND dentro = 0")
	bb = []
	for i in range (0,len(aa)):
		tmp = aa[i]
		tmp2 = tmp[0]
		bb.insert(i,str(tmp2))
		#print(str(bb[i]))
	return bb

def getDireccionesSalir():
	aa = run_query("SELECT MAC FROM parking.Usuarios WHERE Acceso = 'SI' AND dentro = 0")
	bb = []
	for i in range (0,len(aa)):
		tmp = aa[i]
		tmp2 = tmp[0]
		bb.insert(i,str(tmp2))
		#print(str(bb[i]))
	return bb

def regMACEntrada(MAC):
	# Registramos como que el vehiculo se encuentra dentro del parking
	run_query("UPDATE parking.Usuarios SET dentro = 1 WHERE MAC = '"+MAC+"'")

	# Registramos la hora en la otra tabla y el usuario asociado
	t = time.strftime("%H:%M:%S") #Formato de 24 horas
	day = time.strftime("%Y-%m-%d")#yyyy-mm--dd
	datetime = day+' '+t
	#print(t)
	#print(day)

	#print("Fecha/Hora: "+datetime+"\n\n")
    '''
	cc = run_query("SELECT idUsuario FROM parking.Usuarios WHERE MAC='"+MAC+"'")
	cc = cc[0]
	idus = str(cc[0])
	query1 = "INSERT INTO parking.time_table (time, idUsuario) VALUES ('"+datetime+"','"+idus+"');"
	l = run_query(query1)
    '''

def regMACSalida(MAC):
	# Registramos como que el vehiculo se encuentra dentro del parking
	run_query("UPDATE parking.Usuarios SET dentro = 0 WHERE MAC = '"+MAC+"'")

	# Registramos la hora en la otra tabla y el usuario asociado
	t = time.strftime("%H:%M:%S") #Formato de 24 horas
	day = time.strftime("%Y-%m-%d")#yyyy-mm--dd
	#datetime = day+' '+t
	#print(t)
	#print(day)
    '''
	print("Fecha/Hora: "+datetime+"\n\n")

	cc = run_query("SELECT idUsuario FROM parking.Usuarios WHERE MAC='"+MAC+"'")
	cc = cc[0]
	idus = str(cc[0])
	query1 = "INSERT INTO parking.time_table (time, idUsuario) VALUES ('"+datetime+"','"+idus+"');"
	l = run_query(query1)
    '''


def inicializarHCR(trigger, echo):
    GPIO.setup(trigger,GPIO.OUT)  #Configuramos Trigger como salida
    GPIO.setup(echo,GPIO.IN)      #Configuramos Echo como entrada
    GPIO.output(trigger,False)    #Ponemos el pin 25 como LOW
    print("HRC inicializado")

def readHCR(trigger, echo):
    GPIO.output(trigger,True)   #Enviamos un pulso de ultrasonidos
    time.sleep(0.00001)              #Una p pausa
    GPIO.output(trigger,False)  #Apagamos el pulso
    start = time.time()              #Guarda el tiempo actual mediante time.time()
    while GPIO.input(echo)==0:  #Mientras el sensor no reciba seal...
        start = time.time()          #Mantenemos el tiempo actual mediante time.time()
    while GPIO.input(echo)==1:  #Si el sensor recibe seal...
        stop = time.time()           #Guarda el tiempo actual mediante time.time() en otra variable
    elapsed = stop-start             #Obtenemos el tiempo transcurrido entre envio y recepcion
    distance = (elapsed * 34300)/2   #Distancia es igual a tiempo por velocidad partido por 2   D = (T x V)/2
    return distance

#Definicion de descubrimiento de bluetooth device
def discoverNearBluetoothDevices():
    nearby_devices = bluetooth.discover_devices()    #Escanea los dispositivos bluetooth cercanos
    return nearby_devices

# Inquiry de forma infinita
def inquiry(inquirier):
    resultado = None
    while True:
        inquirier.inquiry()
        while inquirier.is_inquiring():
            resultado = inquirier.process_event()
            if(resultado!=None):
                return resultado

def inicializarServo(pin):
    #GPIO.setup(pin,GPIO.OUT)    #Ponemos el pin 21 como salida
    #servo = GPIO.PWM(pin,50)        #Ponemos el pin 21 en modo PWM y enviamos 50 pulsos por segundo
    #servo.start(7.5)
    #servo.ChangeDutyCycle(posServoInicial)               #Ponemos la barrera en posicion icial, bajada
    posServo=posServoInicial
    print("Servo Inicializado")

def subirBarrera():
    if posServo == posServoBajado:
	print("Subiendo barrera... Espere...")
        servo.ChangeDutyCycle(posServoSubido)
    else :
        print "Por favor espere a que se baje la barrera y vuelva a intentarlo"
        #bajarBarrera()

def bajarBarrera():
    if posServo == posServoSubido:
	print("Bajando barrera... Espere...")
        servo.ChangeDutyCycle(posServoBajado)
    else :
        print "Por favor espere a que la barrera suba del todo"
        subirBarrera()

def scanDevices():
    # Obtenemos la ID y el puerto por el que se enviaran los datos
    port = 58978

    # Obtenemos la MAC del dispositivo a partir del ID
    mac = None
    hci_out = Popen(['hcitool', 'dev'], stdout=PIPE).stdout.readlines()

    del hci_out[0]  # 'Devices:\n'

    for dev in hci_out:
        opts = dev[1:-1].split('\t')  # Elimino el primer tabulador y \n y divido
        if not opts[0][:3] == "hci":
            continue

        dev_id = opts[0][3:]
        mac = opts[1]

        # Inicia el inquiry para este Bluetooth
        inquirier = BluezInquiry(int(dev_id), mac, port)
        result = inquiry(inquirier)
        return result

def optimizar(potencias):
    resultado = {}
    for addr in potencias.keys():
        rssi_vect = potencias[addr]
        resultado[addr] = sum(rssi_vect)/len(rssi_vect)

    return resultado

def ordenar(dispositivos):
    resultado = sorted(dispositivos.items(), key=operator.itemgetter(1), reverse=True)
    return resultado

try:
    inicializarServo(servoPinBCM)

    inicializarHCR(TRIGGER1, ECHO1)
    #inicializarHCR(TRIGGER2, ECHO2)
    while True:      #iniciamos un loop infinito

        '''
        print "distance 1 " + readHCR(TRIGGER1, ECHO1)
        #print "distance 2 " + readHCR(TRIGGER2, ECHO2)
        '''

        distance1 = readHCR(TRIGGER1, ECHO1)
        #distance2 = readHCR(TRIGGER2, ECHO2)
        #if distance1 <dmin and distance2 < dmin:
	if distance1 <dmin:
            #print "Vehiculo a menos de " +dmin+ " d1 = "+distance1+" d2 = " +distance2
	    print("Vehiculo a menos de " ,dmin, " d1 = " ,distance1,)
        dispositivos = optimizar(scanDevices())
	    print str(dispositivos)
        print str(getDireccionesEntrar())
        time.sleep(pausa)

except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
    #servo.stop()                      #Detenemos el servo
    GPIO.cleanup()                #Limpiamos los pines GPIO de la Raspberry y cerramos el script
