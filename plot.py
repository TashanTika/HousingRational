# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 23:24:42 2020

@author: Tashan Tika
"""


mapbox_token = "pk.eyJ1IjoibmcxOTg0IiwiYSI6ImNraDlqMHgxZTByY3Ayd256bzlvcXp3OHAifQ.o2MXE6NacffhElGwSRjQIA"

#Read CSV File
import pandas as pd 
import config_p24
sta_df = pd.read_excel(config_p24.coordinates) 

# TO DO refine marker color based on price and add more info in text box (Title, address, size etc.) like here https://docs.mapbox.com/mapbox-gl-js/example/popup-on-hover/

# this data trace shows the listings
from plotly.offline import plot
import plotly.graph_objects as go

scatt = go.Scattermapbox(
                        lat = list(sta_df["lat"]),
                        lon = list(sta_df["lon"]),                        
                        mode='markers',
                        hoverinfo='text',
                        marker=dict(symbol ='marker', size=5, color='blue'),
                        textposition='top right',
                        textfont=dict(size=16, color='black'),
                        text= list(sta_df["Address"])
                        )

# TO DO add trace with crime stats per region chlorochart

layout = go.Layout(hovermode = "closest",
                    mapbox = dict(           
                                 accesstoken= mapbox_token,
                                 zoom=8,
                                 center=dict(lat = sta_df["lat"].median(),
                                             lon = sta_df["lon"].median()
                                             )
                               )
                    )

            
fig=go.Figure(data = [scatt], layout = layout)
plot(fig)

