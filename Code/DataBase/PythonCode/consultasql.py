#import MySQLdb
from __future__ import print_function 
import mysql.connector 
from mysql.connector.constants import ClientFlag 

import sys 
import time

# -*- coding: utf-8 -*-

# Se definen los parametros de la conexion con la base de datos
#DB_HOST = 'localhost' 
#DB_USER = 'sergio' 
#DB_PASS = '123456' 
#DB_NAME = 'parking' 


#  Se crea la funcion que realiza la consulta 
def run_query(query=''): 
    
    config = { 
	    'user': 'root', 
	    'password': '123456', 
	    'host': '127.0.0.1', 
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

# Se ejecuta la consulta
# Ejemplo para MAC_bluetooth = "MAC_1" (La MAC se pasa como string, de momento)
MAC_bluetooth = "MAC_1"

print ("Consulta a Base de Datos: MAC = "+MAC_bluetooth)

b = run_query('SELECT Acceso FROM parking.Usuarios WHERE MAC="%s"' %(MAC_bluetooth))

c = run_query('SELECT idUsuario FROM parking.Usuarios WHERE MAC="%s"' %(MAC_bluetooth))


# b es una tupla, para acceder a los datos es: b[0], b[1], b[2], ...
# En caso de que no exista ese registro de MAC en la base de datos,
# la variable b esta vacia.

if len(b)>0: 
	b = b[0]
	print ("ACCESO PERMITIDO: "+b[0])
if len(b)>0:
	c = c[0]
	idus = str(c[0])
	print ("ID USUARIO: "+idus)



# Decision
if len(b)==0:
    print ("ACCESO NO PERMITIDO: No hay ninguna entrada con esa MAC")
elif '%s'%b[0]=='SI':
    	print ("ACCESO PERMITIDO")
	t = time.strftime("%H:%M:%S") #Formato de 24 horas
	day = time.strftime("%Y-%m-%d")#yyyy-mm--dd
	datetime = day+' '+t
	#print(t)
	#print(day)
	
	print("Fecha/Hora: "+datetime+"\n\n")
	
	query1 = 'INSERT INTO `parking`.`time_table` (`time`, `idUsuario`) VALUES ("'+datetime+'","'+idus+'");'
	l = run_query(query1)
else:
    print ("ACCESO NO PERMITIDO")





