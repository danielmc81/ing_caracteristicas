#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State


# In[ ]:


app = dash.Dash(external_stylesheets=[dbc.themes.YETI])
server = app.server

ds = pd.read_csv("https://raw.githubusercontent.com/danielmc81/ing_caracteristicas/main/datos_limpios.csv") 
ds.drop(["city_hmo","city_nog","city_obr"], axis=1, inplace=True)
ds["date"] = pd.to_datetime(ds.date)


# In[ ]:


dsn = ds.copy()

column = ["HQprcp_hmo","prcp_hmo","HQprcp_nog","prcp_nog","HQprcp_obr","prcp_obr"]
dsn[column] = ds[column]/ds[column].abs().max()


# In[ ]:


dsn_hmo = dsn[["date","HQprcp_hmo","prcp_hmo"]]
dsn_nog = dsn[["date","HQprcp_nog","prcp_nog"]]
dsn_obr = dsn[["date","HQprcp_obr","prcp_obr"]]


# In[ ]:


dsn_hmo = ds[["date","HQprcp_hmo","prcp_hmo"]]
dsn_nog = ds[["date","HQprcp_nog","prcp_nog"]]
dsn_obr = ds[["date","HQprcp_obr","prcp_obr"]]


# In[ ]:


dsn_hmo.rename(columns={"prcp_hmo":"Prometeus","HQprcp_hmo":"Nasa"}, inplace=True)
dsn_nog.rename(columns={"prcp_nog":"Prometeus","HQprcp_nog":"Nasa"}, inplace=True)
dsn_obr.rename(columns={"prcp_obr":"Prometeus","HQprcp_obr":"Nasa"}, inplace=True)


# In[ ]:


def grafica(ds, ciudad):
    fig = px.line(ds, 
                  x=ds["date"], 
                  y=["Prometeus","Nasa"], 
                  labels={"variable": "Pronóstico",
                          "date": "Fecha",
                          "value": "Precip. (mm)"
                         })

    fig.update_xaxes(showgrid=True, visible=True, title_text=ciudad)
    fig.update_yaxes(tickformat=".2f", title_text="Precipitación (mm)")
    
    return fig    


# In[ ]:


def mapa():
    lats = [29.095200, 31.318611, 27.486389]
    lons = [-111.051100, -110.945833, -109.94083]

    nlats = [29.049999, 31.350002, 27.450001]
    nlons = [-111.049995, -110.949997, -109.949997]

    fig = go.Figure(go.Scattermapbox(
        mode = "markers+lines",
        lat = [29.095200, 29.049999],
        lon = [-111.051100, -111.049995],
        marker = {'size': 10}, 
        text=["Prometeus"+'<br>'"Dist. entre abmos 5.01 Km","Nasa"+'<br>'"Dist. entre abmos 5.01 Km"],
        name="Hermosillo"))

    fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
        lat = [31.318611, 31.350002],
        lon = [-110.945833, -110.949997],
        marker = {'size': 10},
        text=["Prometeus"+'<br>'"Dist. entre abmos 3.50 Km","Nasa"+'<br>'"Dist. entre abmos 3.50 Km"],
        name="Heroica Nogales"))

    fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
        lat = [27.486389, 27.450001],
        lon = [-109.94083, -109.949997],
        marker = {'size': 10},
        text=["Prometeus"+'<br>'"Dist. entre abmos 4.13 Km","Nasa"+'<br>'"Dist. entre abmos 4.13 Km"],
        name="Ciudad Obregón"))

    fig.update_layout(
        margin ={'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'center': {'lon': -111, 'lat': 29.5},
             'style': "open-street-map",
            'center': {'lon': -111, 'lat': 29.5},
            'zoom': 6})

#     fig.show()
    return fig


# In[ ]:


app.layout = dbc.Container([
    dbc.Row([
        html.H2("Reporte PROMETEUS"),
        html.H5("Comparación de los pronósticos de precipitación que genera PROMETEUS y la NASA"),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br()
    ]),
    dbc.Row([
        dbc.Col([
            html.H5("Se utilizaron 3 ciudades de Sonora para revisión ya que por el momento solo contamos con información para estas localidades en ambos datasets"),
            html.H5("En la siguiente gráfica podemos ver la poca similitud entre ambos pronósticos."),
            html.H5("Esto es en parte a que los valores de la Nasa estan aproximadamente a 5 Km de los de Prometeus, lo cual es suficiente para que sean tan diferentes"),
            
            html.Br(),
            html.Br()
        ], align="center", lg=4, md=12, xs=12),
        dbc.Col([
            dcc.Dropdown(
                id="menu",
                options=[{"label": "Hermosillo", "value": "dsn_hmo"},
                         {"label": "Heroica Nogales", "value": "dsn_nog"},
                         {"label": "Ciudad Obregón", "value": "dsn_obr"}
                ],
                value="dsn_hmo"                
            ),
            dcc.Graph(
                id="grafica",
                className="dropgraph",                
            )
        ], align="center", lg=8, md=12, xs=12)
    ]),
    dbc.Row([
        dbc.Col([
                html.H5("En el mapa que se presenta, esta graficada la distancia entre los puntos de ambos datasets, tambien se indica la distancia en Km que existe entre ellos"),
                html.H5("Como trabajo futuro podriamos plantear la posibilidad de utilizar la mismas coordenadas de la Nasa en Prometeus para ver si eso mejora la similitud en cuanto a pronóstico"),
                html.Br()
        ], align="center", lg=4, md=12, xs=12),
        dbc.Col([
            dcc.Graph(figure=mapa())
        ], align="center", lg=8, md=12, xs=12)
    ]),
    dbc.Row([
        html.Br(),
    ]),
    dbc.Row([
        html.Br(),        
        html.H5("Toda la información a detalle acerca de como se generó esta informacion ademas de el código para reproducir este tablero se encuentra en el siguiente repositorio https://github.com/danielmc81/ing_caracteristicas.git")
    ])
])

@app.callback(Output("grafica", "figure"),
              Input("menu", "value"))

def grafica(value):
    if value == "dsn_hmo":
        ds = dsn_hmo
        ciudad = "Hermosillo"
    elif value == "dsn_nog":
        ds = dsn_nog
        ciudad = "Heroica Nogales"
    else:
        ds = dsn_obr
        ciudad = "Ciudad Obregón"
        
    fig = px.line(ds, 
                  x=ds["date"], 
                  y=["Prometeus","Nasa"], 
                  labels={"variable": "Pronóstico",
                          "date": "Fecha",
                          "value": "Precip. (mm)"
                         })

    fig.update_xaxes(showgrid=True, visible=True, title_text=ciudad)
    fig.update_yaxes(tickformat=".2f", title_text="Precipitación (mm)")
    
    return fig    

if __name__ == '__main__':
    app.run_server()


# In[ ]:




