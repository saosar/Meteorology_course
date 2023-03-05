#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 01:00:16 2023

@author: soa
"""

# 0. Loading libraries

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr # useful library to handle netCDF4 files
import pandas as pd
import scipy.stats as ss #For statistical functions
import datetime
import os


# 1. Loading the file
ifile="t2m_mon_2011-2015_celsius60.nc" # Below we will use the names of the variable of interest (temperature = Temp2m) and the time variable (dates = time)
                             # You can find these names via previous inspection with "ncdump -h <ifile>"

#_______________________________________________________________________________________________________________________

# 2 : DEFINING THE REGION OVER WHICH THE AVERAGE WILL BE CALCULATED

# =============================================================================
# AREA 1
# =============================================================================
lati1=3.75    #Latitude to the south
lati2=8.25    #Latitude to the north
long1=284.0   #Longitude to the west
long2=288.75  #Longitude to the east

os.system("echo ")
os.system("echo Averages for the region bounded by:")
os.system("echo South lat :"+str(lati1)+" ")
os.system("echo North lat :"+str(lati2)+" ")
os.system("echo West lon :"+str(long1)+" ")
os.system("echo East lon :"+str(long2)+" ")

# Calculation of the spatial average using CDO
# Note that temporary files are generated in the process. 
# These files are deleted during the execution of this script.
os.system("rm -f tmp1.nc fldmean1.nc")
os.system("cdo -f nc -r sellonlatbox,"+str(long1)+","+str(long2)+","+str(lati1)+","+str(lati2)+" " + ifile +" " "tmp1.nc")
os.system("cdo -f nc -r fldmean,weights=TRUE tmp1.nc fldmean1.nc")           
os.system("rm -f tmp1.nc")

# In this section, the temporal files with the spatial averages are loaded:
filename1 = "./fldmean1.nc"      
h1    = xr.open_dataset(filename1) 
f11   = h1.Temp2m [:,:,:].values       
fch1  = h1.time.values	         

ntim1 = fch1.size
f21 = np.reshape(f11, (ntim1,1))
aav1 = f21.flatten()                         

# =============================================================================
# AREA 2
# =============================================================================
lati3=9.0    #Latitude to the south
lati4=13.5   #Latitude to the north
long3=273.75 #Longitude to the west
long4=278.25 #Longitude to the east

os.system("echo ")
os.system("echo Averages for the region bounded by:")
os.system("echo South lat :"+str(lati3)+" ")
os.system("echo North lat :"+str(lati4)+" ")
os.system("echo West lon :"+str(long3)+" ")
os.system("echo East lon :"+str(long4)+" ")

os.system("rm -f tmp2.nc fldmean2.nc")
os.system("cdo -f nc -r sellonlatbox,"+str(long3)+","+str(long4)+","+str(lati3)+","+str(lati4)+" " + ifile +" " "tmp2.nc")
os.system("cdo -f nc -r fldmean,weights=TRUE tmp2.nc fldmean2.nc")           
os.system("rm -f tmp2.nc")

filename2 = "./fldmean2.nc"
h2    = xr.open_dataset(filename2) 
f11   = h2.Temp2m [:,:,:].values       
fch1  = h1.time.values	         

ntim1 = fch1.size
f21 = np.reshape(f11, (ntim1,1))
aav1 = f21.flatten()   



# =============================================================================
# 
# =============================================================================

# 3. GUARDANDO PROMEDIOS ESPACIALES EN UN ARCHIVO ASCII simple
# Ahora guardamos la serie de tiempo del promedio temporal en un archivo ASCII:
aav1name="ts_mi-serie-sencilla_fch.txt"    # Nombre del archivo ASCII de salida
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

#Para hacer una gráfica sencilla del promedio obtenido:
plt.figure(figsize=(15,6.5))
plt.plot(mons2, aav1-273.5, 'black', linewidth=1.0) #la funcion plot de matplotlib nos permite graficar
plt.xlabel("Tiempo") #Definimos el nombre del eje x
plt.xticks(mons2, mons2, rotation='vertical')
plt.ylabel("Temperatura (°C)")
plt.title("Serie de Tiempo Promedio Espacial")
plt.savefig('ts_aave_mi-region_Temp2m_mon.jpg', dpi=600)  #Guardar figura
plt.show()
plt.close()