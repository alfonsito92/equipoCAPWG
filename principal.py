import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep
import bluetooth

GPIO.setmode(GPIO.BCM)   #Ponemos la Raspberry en modo BCM

dmin=40 #Distancia minima de los objetos a los sensores para iniciar un emparejamiento

servoPinBCM = 18
posServoInicial = 1
posServo = 1
posServoSubido = 6
posServoBajado = 1

TRIGGER1 = 21
ECHO1 = 20

TRIGGER2 = 24
ECHO2= 23

pausa=5

#Funciones
def inicializarHCR(trigger, echo):
    GPIO.setup(trigger,GPIO.OUT)  #Configuramos Trigger como salida
    GPIO.setup(echo,GPIO.IN)      #Configuramos Echo como entrada
    GPIO.output(trigger,False)    #Ponemos el pin 25 como LOW

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

def inicializarServo(pin):
    GPIO.setup(pin,GPIO.OUT)    #Ponemos el pin 21 como salida
    servo = GPIO.PWM(pin,50)        #Ponemos el pin 21 en modo PWM y enviamos 50 pulsos por segundo
    servo.start(7.5)
    servo.ChangeDutyCycle(posInicial)               #Ponemos la barrera en posicion icial, bajada
    posServo=posInicial

def subirBarrera():
    if posServo == posServoBajado:
        servo.ChangeDutyCycle(posServoSubido)
    else :
        print "Por favor espere a que se baje la barrera y vuelva a intentarlo"
        bajarBarrera()

def bajarBarrrera():
    if posServo == posServoSubido:
        servo.ChangeDutyCycle(posServoBajado)
    else :
        print "Por favor espere a que la barrera suba del todo"
        subirBarrera()

try:
    inicializarServo(numPinBCM)
    inicializarHCR(TRIGGER1, ECHO1)
    inicializarHCR(TRIGGER2, ECHO2)
    while True:      #iniciamos un loop infinito

        '''
        print "distance 1 " + readHCR(TRIGGER1, ECHO1)
        print "distance 2 " + readHCR(TRIGGER2, ECHO2)
        '''

        distance1 = readHCR(TRIGGER1, ECHO1)
        distance2 = readHCR(TRIGGER2, ECHO2)
        if distance1 <dmin and distance2 < dmin:
            print "Vehiculo a menos de " +dmin+ " d1 = "+distance1+" d2 = "+distance2
            nearDevices = discoverNearBluetoothDevices()
            subirBarrera()
            time.sleep(200)
            bajarBarrera()
        time.sleep(pausa)

except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
    #servo.stop()                      #Detenemos el servo
    GPIO.cleanup()                #Limpiamos los pines GPIO de la Raspberry y cerramos el script