#!/usr/bin/env python
# coding: utf-8

# In[1]:


from netCDF4 import Dataset, num2date
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as crs
from wrf import getvar, get_cartopy, latlon_coords, to_np, cartopy_xlim, cartopy_ylim
import pprint
import pandas as pd 
import os
from datetime import datetime
import seaborn as sns
import dataframe_image as dfi
from geopy.distance import geodesic
from scipy.spatial.distance import cdist, pdist


# #### Función que genera un dataframe a partir de la lectura de un archivo de la NASA

# In[2]:


def get_nasa_dataframe(dataset,idx):
    lats = dataset.variables["lat"][:]
    lons = dataset.variables["lon"][:]
    time = dataset.variables["time"]
    
    times = num2date(time[:], time.units)
    time_of_data = times[0].strftime("%Y-%m-%d")
    
    prcpCal = f1.variables["precipitationCal"]
    prcpCal_cnt = f1.variables["precipitationCal_cnt"]
    prcpCal_cnt_cond = f1.variables["precipitationCal_cnt_cond"]

    HQprcp = f1.variables["HQprecipitation"]
    HQprcp_cnt = f1.variables["HQprecipitation_cnt"]
    HQprcp_cnt_cond = f1.variables["HQprecipitation_cnt_cond"]

    ds = xr.Dataset(
        {
            "date": time_of_data,
            "prcpCal": (("lon", "lat"), prcpCal[0,:,:]),
            "prcpCal_cnt": (("lon", "lat"), prcpCal_cnt[0,:,:]),
            "prcpCal_cnt_cond": (("lon", "lat"), prcpCal_cnt_cond[0,:,:]),
            "HQprcp": (("lon", "lat"), HQprcp[0,:,:]),     
            "HQprcp_cnt": (("lon", "lat"), HQprcp_cnt_cond[0,:,:]),     
            "HQprcp_cnt_cond": (("lon", "lat"), HQprcp_cnt_cond[0,:,:]),             
        },
        {
            "lon": lons,
            "lat": lats,
        },
    )

    df = ds.to_dataframe()    
    dataframe = df.reset_index()[:]
    
    return(dataframe.iloc[idx])


# #### Función que regresa un dataframe solo con la información de precipitación, ciudad y fecha

# In[3]:


def get_prometeus_dataframe(filename, df, city):
    date = filename[:8]
    date = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")    
        
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%d")
    
    dfp_city = df[(df["dominio"] == "d01") & (df["ciudad"] == city)]
    
    dfp_city_date = dfp_city[dfp_city.datetime == date]    
    
    total = dfp_city_date["precipitacion"].sum()
#     print(total)
    
    data = {
            "date": [date],
            "city": [city],
            "precipitation": [total]
            }
    
    df_data = pd.DataFrame(data)

    return(df_data)


# #### En este paso abrimos todos los archivos de la NASA que previamente descargamos, ademas mandamos extraer solo la información de ciertas ciudades. Todos los archivos tiene el prefix NASA GES_DISC GPM_L3 v06 IMERG_Final

# In[4]:


path = "nasa/"
df_nasa = pd.DataFrame()
dfn_hmo = pd.DataFrame()
dfn_nog = pd.DataFrame()
dfn_obr = pd.DataFrame()

for ncfile in os.listdir(path):
    if ncfile.endswith(".nc4"):
        f1 = Dataset(path + ncfile)
        dfn_hmo = dfn_hmo.append(get_nasa_dataframe(f1, 7950), ignore_index=True)
        dfn_nog = dfn_nog.append(get_nasa_dataframe(f1, 5656), ignore_index=True)
        dfn_obr = dfn_obr.append(get_nasa_dataframe(f1, 10336), ignore_index=True)
        f1.close()

dfn_hmo = dfn_hmo.sort_values(by="date").reset_index(drop=True)
dfn_nog = dfn_nog.sort_values(by="date").reset_index(drop=True)
dfn_obr = dfn_obr.sort_values(by="date").reset_index(drop=True)


# #### Revisamos que todo se haya generado bien

# In[5]:


#Hermosillo
dfn_hmo.head()


# In[6]:


#Heroica Nogales
dfn_nog.head()


# In[7]:


#Ciudad Obregon
dfn_obr.head()


# #### En este paso abrimos todos los archivos de PROMETEUS que previamente descargamos, ademas mandamos extraer solo la información de ciertas ciudades. Todos los archivos tiene el prefix fecha+_dataset.csv

# In[8]:


path = "prometeus/"
dfp_nog = pd.DataFrame()
dfp_hmo = pd.DataFrame()
dfp_obr = pd.DataFrame()

for file in os.listdir(path):
    if file.endswith(".csv"):
        f1 = pd.read_csv(path + file)        
        dfp_nog = dfp_nog.append(get_prometeus_dataframe(file, f1, "Heroica Nogales"), ignore_index=True)
        dfp_hmo = dfp_hmo.append(get_prometeus_dataframe(file, f1, "Hermosillo"), ignore_index=True)
        dfp_obr = dfp_obr.append(get_prometeus_dataframe(file, f1, "Ciudad Obregón"), ignore_index=True)
        
dfp_nog = dfp_nog.sort_values(by=["date"]).reset_index(drop=True)
dfp_hmo = dfp_hmo.sort_values(by=["date"]).reset_index(drop=True)
dfp_obr = dfp_obr.sort_values(by=["date"]).reset_index(drop=True)


# #### Revisamos que todo se haya generado bien

# In[9]:


#Heroica Nogales
dfp_nog.head()


# In[10]:


#Hermosillo
dfp_hmo.head()


# In[11]:


#Ciudad Obregón
dfp_obr.head()


# #### Unimos los dataframes de NASA y PROMETEUS para cada ciudad

# In[12]:


adata_hmo = dfn_hmo.merge(dfp_hmo, on=["date"], how="left") 
adata_nog = dfn_nog.merge(dfp_nog, on=["date"], how="left")
adata_obr = dfn_obr.merge(dfp_obr, on=["date"], how="left")


# #### Revisamos que se hayan generado bien

# In[13]:


#Hermosillo
adata_hmo.head()


# In[14]:


#Heroica Nogales
adata_nog.head()


# In[15]:


#Ciudad Obregon
adata_obr.head()


# #### Unimos los 3 dataframes

# In[27]:


adata_merged = pd.merge(adata_hmo, adata_nog, on="date", suffixes=("_hmo","_nog"))
adata = pd.merge(adata_merged, adata_obr, on="date")


# #### Revisamos que esten todos los datos

# In[28]:


adata.info()


# #### Por último generamos el archvo tidy_data.csv para trabajar con el mas adelante

# In[29]:


#Renombramos las columnas para que tengan el mismo formato
adata.rename(columns = {"city": "city_obr", 
                        'HQprcp': 'HQprcp_obr', 
                        "precipitation": "prcp_obr", 
                        "precipitation_hmo": "prcp_hmo",
                        "precipitation_nog": "prcp_nog"},
             inplace = True)

sel_adata = adata[["date","city_hmo","city_nog","city_obr",
                   "HQprcp_hmo","HQprcp_nog","HQprcp_obr",
                   "prcp_hmo","prcp_nog","prcp_obr"]]

sel_adata.to_csv("datos_tidy.csv", index=False)


# In[ ]:




