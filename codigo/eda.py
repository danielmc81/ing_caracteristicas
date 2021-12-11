#!/usr/bin/env python
# coding: utf-8

# ## Análisis Exploratorio de Datos

# In[34]:


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


# #### Lectura de los datos limpios

# In[35]:


ds = pd.read_csv("datos_limpios.csv") 
ds


# In[36]:


ds.info()


# In[37]:


ds.isnull().sum()


# In[38]:


ds.describe()


# #### Podemos observar varias cosas, En Nogales es mayor el pronóstico de lluvia en comparación con las otras ciudades. Podemos ver que tiene un pronóstico de lluvia de 4mm y una desviación de 11, un poco alta. También el valor maximo fue dado para Nogales por PROMETEUS. En general, PROMETEUS da un pronóstico mas elevado en precipitación.
# 

# In[39]:


ds


# In[40]:


#Histograma de "HQprcp"

sns.histplot(data=ds[["HQprcp_hmo","prcp_hmo"]], bins=10)
plt.title("Precipitación diaria acumulada en alta calidad\nNASA", fontsize=12)
plt.xlabel("mm\nHermosillo", fontsize=12)
plt.ylabel("Días con lluvia", fontsize=12)


# In[41]:


sns.histplot(data=ds[["HQprcp_nog","prcp_nog"]], bins=10)
plt.title("Precipitación diaria acumulada en alta calidad\nNASA", fontsize=12)
plt.xlabel("mm\nHeroica Nogales", fontsize=12)
plt.ylabel("Días con lluvia", fontsize=12)


# In[42]:


sns.histplot(data=ds[["HQprcp_obr","prcp_obr"]], bins=10)
plt.title("Precipitación diaria acumulada en alta calidad\nNASA", fontsize=12)
plt.xlabel("mm\nCiudad Obregón", fontsize=12)
plt.ylabel("Días con lluvia", fontsize=12)


# #### Busqueda de correlación de los datos

# In[44]:


sns.heatmap(ds.corr(), annot=True)


# #### Curiosamente podemos observar que existe una correlación entre Hermosillo y Ciudad Obregón. 
