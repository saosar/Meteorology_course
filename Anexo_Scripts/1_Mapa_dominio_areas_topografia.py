#!/usr/bin/env python
# coding: utf-8

"""
Descripción: Este script lee la información contenida en archivos NetCDF de topografía derivados 
del conjunto de datos ERA5 descargados del cds (https://cds.climate.copernicus.eu/#!/home). 


"""

# =============================================================================
# #Cargamos las librerías 
# =============================================================================
import numpy as np #Librería para operaciones numéricas
import matplotlib.pyplot as plt #Librería para generar gráficas 
import cartopy #librería para pintar mapas
import cartopy.crs as ccrs
import xarray as xr #librería para el manejo de archivos NetCDF


#############################################################

# 1 CARGAR EL ARCHIVO NETCDF
datos = xr.open_dataset('heightmask.nc') #Se carga el archivo NetCDF
z = (datos.z)  #
lats = datos.latitude #tomamos los datos de la variable latitud
lons = datos.longitude #tomamos los datos de la variable longitud
time = datos.time
print(len(time))


###############################################################

#2 CONFIGURAR PARA GRAFICAR
  
    #Mapas de SST
fig = plt.figure(figsize=(20,10)) #Abrimos una hoja para pintar nuestro mapa y damos le tamaño a la hoja

ax = fig.add_subplot(projection=ccrs.PlateCarree()) #Indicamos que crearemos un mapa en nuestra hoja
#ax.set_extent([-10, -110, -13, 15]) #Se indican las coordenadas del mapa: lon1, lon2, lat1, lat2
ax.coastlines('50m',linewidth = 1.5) #se agregan los continentes
ax.add_feature(cartopy.feature.BORDERS) #Se agregan los países 
niveles = (0.5,1,2,3,50,100,250,500,750,1000,1250,1500,1750,2000,2500,3000,3500) #np.arange(15,30,1) #Indicamos los valores que tomará la variable y el intervalo de paso
mapa = plt.contourf(lons, lats, z[0,:,:],niveles,cmap="terrain",extend='both') #Pintamos el mapa
contours=plt.contour(lons, lats, z[0,:,:],niveles, colors="black",extend='both') #Agregamos los contornos
plt.clabel(contours, inline=1, fontsize=10, fmt="%i")
#plt.clim = (250,4500) #límites de la paleta de colores
plt.colorbar(mapa, orientation="vertical",shrink=0.75) #Agregamos la paleta de colores
otitle = "Topografia"     # Texto para el título.
plt.title(otitle, size=20, loc='center', pad=8) #Agregamos título al mapa
#plt.title('2010', size=18, loc='right', pad=8)  

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
lat1=1.5    #Latitud más al sur
lat2=9.0    #Latitud más al norte
lon1=283.0   #Longitud más al oeste 
lon2=290.5  #Longitud más al este
ax.plot([lon1, lon2],[lat2, lat2], '-r', transform=ccrs.PlateCarree())
ax.plot([lon2, lon2],[lat1, lat2], '-r', transform=ccrs.PlateCarree())
ax.plot([lon1, lon2],[lat1, lat1], '-r', transform=ccrs.PlateCarree())
ax.plot([lon1, lon1],[lat1, lat2], '-r', transform=ccrs.PlateCarree())

# =============================================================================
# SEGUNDA ÁREA DE INTERÉS
# =============================================================================
# Dibujar líneas para completar un rectángulo
# entre las longitudes lon1 y lon2, y lat1 y lat2. 
lat1=-8.0    #Latitud más al sur  -----
lat2=-0.5   #Latitud más al norte ----
lon1=294.0   #Longitud más al oeste  |||
lon2=301.5  #Longitud más al este   |||
ax.plot([lon1, lon2],[lat2, lat2], '-r', transform=ccrs.PlateCarree())
ax.plot([lon2, lon2],[lat1, lat2], '-r', transform=ccrs.PlateCarree())
ax.plot([lon1, lon2],[lat1, lat1], '-r', transform=ccrs.PlateCarree())
ax.plot([lon1, lon1],[lat1, lat2], '-r', transform=ccrs.PlateCarree())
# =============================================================================

ofile = "height" 
plt.savefig( ofile + '.png') #Guardamos la figura

