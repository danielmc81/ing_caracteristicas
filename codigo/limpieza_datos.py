#!/usr/bin/env python
# coding: utf-8

# ## Limpieza de Datos

# In[7]:


from netCDF4 import Dataset, num2date
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as crs
import pprint
import pandas as pd 
import os
from datetime import datetime
import seaborn as sns
import dataframe_image as dfi
from geopy.distance import geodesic
from scipy.spatial.distance import cdist, pdist
from scipy import stats


# #### Lectura de los datos tidy

# In[8]:


ds = pd.read_csv("datos_tidy.csv") 
ds


# In[9]:


#date tiene formato correcto
ds.info()


# In[10]:


#Convertir date to datetime
ds["date"] = pd.to_datetime(ds.date)

#Convertir city_hmo, city_nog, city_obr a category
ds["city_hmo"] = ds["city_hmo"].astype('category')
ds["city_nog"] = ds["city_nog"].astype('category')
ds["city_obr"] = ds["city_obr"].astype('category')
ds.info()


# #### Búsqueda de valores faltantes

# In[11]:


#Se puede observar que hay 21 renglones faltantes en algunas características
ds.isnull().sum()


# #### Imputación de datos faltantes, primero observaremos los renglones en los cuales existen datos faltantes. Revisando en los archivos pudimos corroborar que no existen los datos para esas fechas en especifico de los datasets de PROMETEUS

# In[12]:


is_nan = ds.isnull()
nan_rows = is_nan.any(axis=1)

ds[nan_rows]


# #### Para los datos de precipitación utilizaremos un metodo de interpolación, para los de las ciudades solamente asignaremos el nombre de la ciudad faltante

# In[13]:


ds.prcp_hmo.interpolate(limit_direction="both", inplace=True)
ds.prcp_nog.interpolate(limit_direction="both", inplace=True)
ds.prcp_obr.interpolate(limit_direction="both", inplace=True)


# #### Ya podemos observar que se modificaron los valores de precipitación

# In[14]:


ds[nan_rows]


# In[15]:


ds["city_hmo"] = ds["city_hmo"].fillna(value="Hermosillo")
ds["city_nog"] = ds["city_nog"].fillna(value="Heroica Nogales")
ds["city_obr"] = ds["city_obr"].fillna(value="Ciudad Obregón")


# #### En este punto han desaparecido los valores NaN

# In[16]:


ds[nan_rows]


# ### Detección de Anomalías utilizando Z-score

# In[17]:


sel_ds = ds.select_dtypes(include=np.number)
sel_ds


# In[18]:


z = np.abs(stats.zscore(sel_ds))
threshold = 3
print(np.where(z > 3))


# ##### Al parecer detecta outliers pero pueden ser valores esperados ya que se trata de precipitación acumulada en 24 horas.

# In[19]:


print(z[114][3])


# In[20]:


print(sel_ds.iloc[93][1])


# In[21]:


pd.set_option('display.max_rows', None)
sel_ds


# #### Podemos visualizar mejor con graficas de caja

# In[22]:


# Agrupar cada 15 dias y generar un boxplot para HQprcp y precipitation
dg = ds.groupby(pd.Grouper(key="date", freq="15d")).sum()


# In[23]:


sns.boxplot(data = dg[["HQprcp_hmo","HQprcp_nog","HQprcp_obr"]])
plt.title("Precipitación diaria acumulada en alta calidad\nNASA", fontsize=12)
plt.xlabel("\nPrecipitación", fontsize=12)
plt.ylabel("mm", fontsize=12)


# In[24]:


sns.boxplot(data = dg[["prcp_hmo","prcp_nog","prcp_obr"]])
plt.title("Precipitación diaria acumulada en alta calidad\nPROMETEUS", fontsize=12)
plt.xlabel("\nPrecipitación", fontsize=12)
plt.ylabel("mm", fontsize=12)


# #### Revisando las estadísticas podemos ver que no necesariamente se tratan de outlier, ya que la maxima que se presento fue de 41 mm en el pronóstico de PROMETEUS. 

# In[25]:


ds.describe()


# #### Como conclusión podemos determinar dejar tal cual estan los datos, al no considerarlos como atípicos

# #### Guardamos el dataframe  a un archivo para despues aplicarle el EDA

# In[26]:


ds.to_csv("datos_limpios.csv", index=False)

