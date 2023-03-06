# -*- coding: utf-8 -*-
"""

Descripcion: Este script te permite graficar series de tiempo, calcular ciclos diurnos mensuales y 
graficarlos 

"""

# 0. Cargando librerías

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr #libreria util para tratar con archivos netCDF4
import pandas as pd
import scipy.stats as ss #Para funciones estadisticas
import datetime
import os


# 1. Cargando el archivo
ifile="prom_estacional_multianual_mnssns.nc" # Abajo se usarán los nombres de la variable de interés (temperatura = Temp2m ) y de la variable tiempo (fechas = time)
                             # Estos nombres puede averiguarlos via inspección previa con "ncdump -h <ifile>"

#_______________________________________________________________________________________________________________________

# 2 : SE DEFINEN LAS REGIÓN SOBRE LA QUE SE HARÁ EL PROMEDIO

# =============================================================================
# ÁREA 1
# =============================================================================
lati1=2.0    #Latitud más al sur
lati2=9.0    #Latitud más al norte
long1=283.0   #Longitud más al oeste 
long2=290.0  #Longitud más al este

os.system("echo ")
os.system("echo Promedios para Región limitada por:")
os.system("echo South lat :"+str(lati1)+" ")
os.system("echo North lat :"+str(lati2)+" ")
os.system("echo West lon :"+str(long1)+" ")
os.system("echo East lon :"+str(long2)+" ")

# A continuación se hace el cálculo del promedio espacial con CDO
# Note que se generan unos archivos temporales en el proceso. 
# Estos archivos se borran durante la ejecución de este script.
os.system("rm -f tmp.nc fldmean.nc")
os.system("cdo -f nc -r  sellonlatbox,"+str(long1)+","+str(long2)+","+str(lati1)+","+str(lati2)+" " + ifile +" " "tmp.nc")
os.system("cdo -f nc -r  fldmean,weights=TRUE tmp.nc fldmean.nc")           # Usamos fldmean para hallar el valor medio, teniendo en cuenta latitudes e ignorando missing values.
os.system("rm -f tmp.nc")


# En esta sección se carga el archivo temporal con los promedios espaciales: 
filename = "./fldmean.nc"        # Archivo temporal con los promedios espaciales
h    = xr.open_dataset(filename) # Esta es una de las formas de abrir un archivo. Se buscará en el objeto "h".
f1   = h.Temp2m [:,:,:].values       # Se cargan los valores de la variable "Temp2m " de "h" a la variable "f1" de este script.   Nombres de variables igual que en ifile arriba.
fch  = h.time.values	         # Se cargan los valores de la variable "time" de "h" a la variable "fch" de este script. Nombres de variables igual que en ifile arriba.

ntim = fch.size
f2 = np.reshape(f1, (ntim,1))
aav1 = f2.flatten()                         # En este arreglo está almacenada la serie de tiempo con los promedios espaciales.

# 3. GUARDANDO PROMEDIOS ESPACIALES EN UN ARCHIVO ASCII simple
# Ahora guardamos la serie de tiempo del promedio temporal en un archivo ASCII:
aav1name="ts_mi-serie-sencilla_fch_area1_4PASOS.txt"    # Nombre del archivo ASCII de salida
os.system("rm -f "+aav1name)                   # Borramos el archivo, si es que existe previamente.  Esto evita que se crezca un archivo previo.
fl = open(aav1name,'w')
for i in range(len(aav1)):
	fl.write("%8.4f\n" % (aav1[i]))        # Guardamos los valores línea por línea. %8.4f guardará valores con 8 posiciones, 4 decimales.  
fl.close()
os.system("rm -f fldmean.nc") # En esta línea estamos borrando el archivo nc temporal 

print(" ")
print("Serie con promedios espaciales guardada archivo ASCII")
print(" ")



# 4. GRAFICANDO LA SERIE DE TIEMPO

# En esta sección seleccionamos información de los pasos de tiempo para ponerlos
# como labels en la gráfica de la serie de tiempo.
# El paso de tiempo o timestamp puede tener información del año, mes, dia, hora, minuto, etc.
# En el siguiente ejemplo solo vamos a seleccionar el año y el mes para formar
# los xticks que irán en el eje X de la serie de tiempo que graficaremos al final. 
# Pero extraemos por separado el año, mes, día, hora, minuto: 
    # así que usted puede usar diferentes combinaciones para las xticks. 

mons2 = []
for kk in range(len(fch)):
	date=pd.to_datetime(fch[kk])       # Atributos de la salida: date.year, date.month, date.day, date.hour, date.minute, date.second
	year   = str(date.year)            # Convirtiendo date.year a un string. El resultado será usado para títulos y nombres en archivos de salida.
	month  = str(date.month).zfill(2)  # Convirtiendo date.month a un string, con ceros al principio cuando mes es un solo dígito. Usar en títulos y nombres en archivos de salida.
	day    = str(date.day).zfill(2)    # Convirtiendo date.day a un string, con ceros al principio cuando mes es un solo dígito. Para usar en títulos y nombres en archivos de salida.
	hour   = str(date.hour).zfill(2)   # Convirtiendo date.hour a un string, con ceros al principio cuando mes es un solo dígito. Para usar entítulos y nombres en archivos de salida.
	minute = str(date.minute).zfill(2) # Convirtiendo date.minute a un string, con ceros al principio cuando mes es un solo dígito. Para usar en títulos y nombres en archivos de salida.
	second = str(date.second).zfill(2) # Convirtiendo date.second a un string, con ceros al principio cuando mes es un solo dígito. Para usar en títulos y nombres en archivos de salida.
# En nuestro ejemplo, solo usaremos el año y el mes para las xticks:
	yymo = year + month                # Concatenando año y mes. El string resultante tiene la forma YYYYMM (e.g. 201112 cuando el año es 2011 y el mes es Diciembre)
	mons2.append(yymo)
    
mons3=["DEF","MAM","JJA","SON"]

#Para hacer una gráfica sencilla del promedio obtenido:
plt.figure(figsize=(15,6.5))
plt.plot(mons2, aav1, 'black', linewidth=1.0) #la funcion plot de matplotlib nos permite graficar
plt.xlabel("Tiempo") #Definimos el nombre del eje x
plt.xticks(mons2, mons3, rotation='vertical') #Cambiamos las cositas de los nombres del eje  x
plt.ylabel("Temperatura (°C)")
plt.title("Serie de Tiempo Promedio Espacial - Área 1")
plt.savefig('serie_tiempo_ciclo_anual_area_1_4PASOS.jpg', dpi=600)  #Guardar figura
plt.show()
plt.close()

# =============================================================================
# AREA 2
# =============================================================================
lati3=-8.0    #Latitud más al sur  -----
lati4=-1.0   #Latitud más al norte ----
long3=294.0   #Longitud más al oeste  |||
long4=301.0  #Longitud más al este   |||


os.system("echo ")
os.system("echo Promedios para Región limitada por:")
os.system("echo South lat :"+str(lati3)+" ")
os.system("echo North lat :"+str(lati4)+" ")
os.system("echo West lon :"+str(long3)+" ")
os.system("echo East lon :"+str(long4)+" ")

# A continuación se hace el cálculo del promedio espacial con CDO
# Note que se generan unos archivos temporales en el proceso. 
# Estos archivos se borran durante la ejecución de este script.
os.system("rm -f tmp.nc fldmean2.nc")
os.system("cdo -f nc -r  sellonlatbox,"+str(long3)+","+str(long4)+","+str(lati3)+","+str(lati4)+" " + ifile +" " "tmp.nc")
os.system("cdo -f nc -r  fldmean,weights=TRUE tmp.nc fldmean2.nc")           # Usamos fldmean para hallar el valor medio, teniendo en cuenta latitudes e ignorando missing values.
os.system("rm -f tmp.nc")


# En esta sección se carga el archivo temporal con los promedios espaciales: 
filename = "./fldmean2.nc"        # Archivo temporal con los promedios espaciales
h    = xr.open_dataset(filename) # Esta es una de las formas de abrir un archivo. Se buscará en el objeto "h".
f1   = h.Temp2m [:,:,:].values       # Se cargan los valores de la variable "Temp2m " de "h" a la variable "f1" de este script.   Nombres de variables igual que en ifile arriba.
fch  = h.time.values	         # Se cargan los valores de la variable "time" de "h" a la variable "fch" de este script. Nombres de variables igual que en ifile arriba.

ntim = fch.size
f2 = np.reshape(f1, (ntim,1))
aav2 = f2.flatten()                         # En este arreglo está almacenada la serie de tiempo con los promedios espaciales.

# 3. GUARDANDO PROMEDIOS ESPACIALES EN UN ARCHIVO ASCII simple
# Ahora guardamos la serie de tiempo del promedio temporal en un archivo ASCII:
aav2name="ts_mi-serie-sencilla_fch_area2_4PASOS.txt"    # Nombre del archivo ASCII de salida
os.system("rm -f "+aav2name)                   # Borramos el archivo, si es que existe previamente.  Esto evita que se crezca un archivo previo.
fl = open(aav2name,'w')
for i in range(len(aav2)):
	fl.write("%8.4f\n" % (aav2[i]))        # Guardamos los valores línea por línea. %8.4f guardará valores con 8 posiciones, 4 decimales.  
fl.close()
os.system("rm -f fldmean2.nc") # En esta línea estamos borrando el archivo nc temporal 

print(" ")
print("Serie con promedios espaciales guardada archivo ASCII")
print(" ")



# 4. GRAFICANDO LA SERIE DE TIEMPO

# En esta sección seleccionamos información de los pasos de tiempo para ponerlos
# como labels en la gráfica de la serie de tiempo.
# El paso de tiempo o timestamp puede tener información del año, mes, dia, hora, minuto, etc.
# En el siguiente ejemplo solo vamos a seleccionar el año y el mes para formar
# los xticks que irán en el eje X de la serie de tiempo que graficaremos al final. 
# Pero extraemos por separado el año, mes, día, hora, minuto: 
    # así que usted puede usar diferentes combinaciones para las xticks. 

mons2 = []
for kk in range(len(fch)):
	date=pd.to_datetime(fch[kk])       # Atributos de la salida: date.year, date.month, date.day, date.hour, date.minute, date.second
	year   = str(date.year)            # Convirtiendo date.year a un string. El resultado será usado para títulos y nombres en archivos de salida.
	month  = str(date.month).zfill(2)  # Convirtiendo date.month a un string, con ceros al principio cuando mes es un solo dígito. Usar en títulos y nombres en archivos de salida.
	day    = str(date.day).zfill(2)    # Convirtiendo date.day a un string, con ceros al principio cuando mes es un solo dígito. Para usar en títulos y nombres en archivos de salida.
	hour   = str(date.hour).zfill(2)   # Convirtiendo date.hour a un string, con ceros al principio cuando mes es un solo dígito. Para usar entítulos y nombres en archivos de salida.
	minute = str(date.minute).zfill(2) # Convirtiendo date.minute a un string, con ceros al principio cuando mes es un solo dígito. Para usar en títulos y nombres en archivos de salida.
	second = str(date.second).zfill(2) # Convirtiendo date.second a un string, con ceros al principio cuando mes es un solo dígito. Para usar en títulos y nombres en archivos de salida.
# En nuestro ejemplo, solo usaremos el año y el mes para las xticks:
	yymo = year + month                # Concatenando año y mes. El string resultante tiene la forma YYYYMM (e.g. 201112 cuando el año es 2011 y el mes es Diciembre)
	mons2.append(yymo)

#Para hacer una gráfica sencilla del promedio obtenido:
plt.figure(figsize=(15,6.5))
plt.plot(mons2, aav2, 'black', linewidth=1.0) #la funcion plot de matplotlib nos permite graficar
plt.xlabel("Tiempo") #Definimos el nombre del eje x
plt.xticks(mons2, mons3, rotation='vertical') #Cambiamos las cositas de los nombres del eje  x
plt.ylabel("Temperatura (°C)")
plt.title("Serie de Tiempo Promedio Espacial - Área 2")
plt.savefig('serie_tiempo_ciclo_anual_area_2_4PASOS.jpg', dpi=600)  #Guardar figura
plt.show()
plt.close()

# =============================================================================
# 2 AREAS EN UN SOLO GRÁFICO
# =============================================================================

#Para hacer una gráfica sencilla del promedio obtenido:
plt.figure(figsize=(15,6.5))
plt.plot(mons2, aav1, aav2, 'black', linewidth=1.0) #la funcion plot de matplotlib nos permite graficar
plt.xlabel("Tiempo") #Definimos el nombre del eje x
plt.xticks(mons2, mons3, rotation='vertical') #Cambiamos las cositas de los nombres del eje  x
plt.ylabel("Temperatura (°C)")
plt.title("Serie de Tiempo Promedio Espacial - Área combinada")
plt.legend(["Área 1","Área 2"],loc=1)
plt.savefig('serie_tiempo_ciclo_anual_area_combinada_4PASOS.jpg', dpi=600)  #Guardar figura
plt.show()
plt.close()






