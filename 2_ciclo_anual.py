#!/usr/bin/env python
# coding: utf-8

"""

Basado en original por Juan Manuel Sánchez - juan.sanchez43@udea.edu.co
"""

# =============================================================================
# Cargamos las librerías 
# =============================================================================
import numpy as np #Librería para operaciones numéricas
import matplotlib.pyplot as plt #Librería para generar gráficas 
import cartopy #librería para pintar mapas
import cartopy.crs as ccrs
import xarray as xr #librería para el manejo de archivos NetCDF
import pandas as pd

# =============================================================================
# Cargar y abrir  
# =============================================================================
# 1 CARGAR EL ARCHIVO NETCDF
datos = xr.open_dataset('heightmask.nc') #Se carga el archivo NetCDF
z = (datos.z)  #
lats = datos.latitude #tomamos los datos de la variable latitud
lons = datos.longitude #tomamos los datos de la variable longitud
time = datos.time
print(len(time))
   
# 2 CARGAR ARCHIVO TEMPERATURA
ifile = xr.open_dataset('t2m_mon_2011-2015_ciclo_anual.nc') # Se carga el archivo NetCDF
Temp2m = ifile.Temp2m #Del archivo tomamos los datos la variable "Temp2m" los cuales ya se encuentran en °C
lat_Temp2m = ifile.latitude #tomamos los datos de la variable latitud
lon_Temp2m = ifile.longitude #tomamos los datos de la variable longitud
times = ifile.time.values  # Lee los tiempos en formato original
dates = pd.to_datetime(times) # Convierte los tiempos a datetime

# Seleccionar un periodo en particular, para el año 2015, visto con cdo info ...
xsel = Temp2m.sel(time=slice('2015-01-01','2015-12-01'))
xdates = pd.to_datetime(xsel.time.values)

for kki in range(len(xdates)):

	# Esta pequeña sección lee la fecha directamente del archivo.
	# Note que leemos todas las componentes de la fecha (año, mes, dia, hora, segundo),
	# pero en este ejemplo sólo usamos el año y el mes, tanto en el título de la gráfica como en el nombre del archivo de salida.
    fecha  = xdates[kki]                # Atributos de la salida: date.year, date.month, date.day, date.hour, date.minute, date.second
    anio   = str(fecha.year)            # Convirtiendo date.year a un string. El resultado será usado para títulos y nombres en archivos de salida.
    mes    = str(fecha.month).zfill(2)  # Convirtiendo date.month a un string, con ceros al principio cuando mes es un solo dígito. Usar en títulos y nombres en archivos de salida.
    dia    = str(fecha.day).zfill(2)    # Convirtiendo date.day a un string, con ceros al principio cuando mes es un solo dígito. Para usar en títulos y nombres en archivos de salida.
    hora   = str(fecha.hour).zfill(2)   # Convirtiendo date.hour a un string, con ceros al principio cuando mes es un solo dígito. Para usar entítulos y nombres en archivos de salida.
    minuto = str(fecha.minute).zfill(2) # Convirtiendo date.minute a un string, con ceros al principio cuando mes es un solo dígito. Para usar en títulos y nombres en archivos de salida.
    segundo = str(fecha.second).zfill(2) # Convirtiendo date.second a un string, con ceros al principio cuando mes es un solo dígito. Para usar en títulos y nombres en archivos de salida.
    yymo = anio + "-" + mes                # Concatenando año y mes. El string resultante tiene la forma YYYY-MM (e.g. 2015-09 cuando el año es 2015 y el mes es Septiembre)
    print("yymo: ",yymo)

    
    # Empezamos a hacer los mapas del periodo seleccionado, uno por uno:
    fig = plt.figure(figsize=(18,10)) #Abrimos una hoja para pintar nuestro mapa y damos le tamaño a la hoja

    ax = fig.add_subplot(projection=ccrs.PlateCarree()) #Indicamos que crearemos un mapa en nuestra hoja
    #ax.set_extent([-10, -110, -13, 15]) #Se indican las coordenadas del mapa
    ax.coastlines('50m',linewidth = 1.5) #se agregan los continentes
    ax.add_feature(cartopy.feature.BORDERS) #Se agregan los países 
    
    
    #NIVELES PARA TEMPERATURA
    niveles_Temp2m = np.arange(15,30,1) #Indicamos los valores que tomará la variable y el intervalo de paso
    mapa = plt.contourf(lon_Temp2m, lat_Temp2m, xsel[kki,:,:],niveles_Temp2m,cmap="jet",extend='both') #Pintamos el mapa
    
    
# =============================================================================
#     #NIVELES PARA TOPOGRAFIA
# =============================================================================
    niveles_Topo = (0.5,1,2,3,50,100,250,500,750,1000,1250,1500,1750,2000,2500,3000,3500) #np.arange(15,30,1) #Indicamos los valores que tomará la variable y el intervalo de paso
    contours=plt.contour(lons, lats, z[0,:,:],niveles_Topo, colors="black",extend='both') #Agregamos los contornos
    plt.clabel(contours, inline=1, fontsize=10, fmt="%i")
# =============================================================================
    
    plt.clim = (15,30) #límites de la paleta de colores
    plt.colorbar(mapa, orientation="vertical",shrink=0.75) #Agregamos la paleta de colores
    plt.title('Temperatura 2m (°C) ' + '2011-2015 mes ' + mes, size=20, loc='center', pad=8) #Agregamos título al mapa
    #plt.title(anio, size=18, loc='right', pad=8)   #año parte superficial

    #Agregamos el grid
    gl= ax.gridlines(color="black",draw_labels=True,linestyle="--")
    #gl.xlabels_top=False #omitimos las etiquetas en la parte superior del mapa
    gl.top_labels=False #omitimos las etiquetas en la parte superior del mapa
    #gl.ylabels_right=False #omitimos las etiquetas en la parte derecha del mapa
    gl.right_labels=False #omitimos las etiquetas en la parte derecha del mapa    
    gl.xlines=False #Omitimos las líneas de latitud
    gl.ylines=False #Omitimos las líneas de longitud 
    gl.xlabel_style = {'size': 15} #Tamaño etiquetas eje X 
    gl.ylabel_style = {'size': 15} #Tamaño etiquetas eje Y
    
    
    # =============================================================================
    # PRIMERA ÁREA DE INTERÉS
    # =============================================================================
    # Dibujar líneas para completar un rectángulo
    # entre las longitudes lon1 y lon2, y lat1 y lat2. 
    lat1=3.75    #Latitud más al sur
    lat2=8.25    #Latitud más al norte
    lon1=284.0   #Longitud más al oeste 
    lon2=288.75  #Longitud más al este
    ax.plot([lon1, lon2],[lat2, lat2], '-r', transform=ccrs.PlateCarree())
    ax.plot([lon2, lon2],[lat1, lat2], '-r', transform=ccrs.PlateCarree())
    ax.plot([lon1, lon2],[lat1, lat1], '-r', transform=ccrs.PlateCarree())
    ax.plot([lon1, lon1],[lat1, lat2], '-r', transform=ccrs.PlateCarree())

    # =============================================================================
    # SEGUNDA ÁREA DE INTERÉS
    # =============================================================================
    # Dibujar líneas para completar un rectángulo
    # entre las longitudes lon1 y lon2, y lat1 y lat2. 
    lat1=-8.25    #Latitud más al sur  -----
    lat2=-3.75   #Latitud más al norte ----
    lon1=291.0   #Longitud más al oeste  |||
    lon2=295.75  #Longitud más al este   |||
    ax.plot([lon1, lon2],[lat2, lat2], '-r', transform=ccrs.PlateCarree())
    ax.plot([lon2, lon2],[lat1, lat2], '-r', transform=ccrs.PlateCarree())
    ax.plot([lon1, lon2],[lat1, lat1], '-r', transform=ccrs.PlateCarree())
    ax.plot([lon1, lon1],[lat1, lat2], '-r', transform=ccrs.PlateCarree())
    # =============================================================================

    plt.savefig('t2m_'  + yymo + '.png',dpi=300) #Guardamos la figura

