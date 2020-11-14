# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 14:23:01 2020
@author: Working Rational
"""

import logging   
import log_init 
import pandas as pd 
import conf

#read data
logging.info("read raw file")
from pathlib import Path
import os

root_dir = Path(__file__).resolve().parent
raw_file = os.path.join(root_dir, 'osm_cleaned.csv')
raw_df = pd.read_csv(raw_file)  

#remove places without coordinates
sta_df = raw_df.loc[~(raw_df["lat"].isna())]
sta_df = raw_df.loc[~(raw_df["lon"].isna())]
removed_rec = raw_df.shape[0] - sta_df.shape[0]
if removed_rec > 0:
    logging.info("there were {} records out of {} records without coordinates ".format(str(removed_rec), str(raw_df.shape[0])))

# plot basic data
logging.info("plotting listings")
from plotly.offline import plot
import plotly.graph_objects as go

# TO DO refine marker color based on price and add more info in text box (Title, address, size etc.) like here https://docs.mapbox.com/mapbox-gl-js/example/popup-on-hover/
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

layout = go.Layout(hovermode = "closest",
                    mapbox = dict(           
                                 accesstoken= conf.mapbox_token,
                                 zoom=8,
                                 center=dict(lat = sta_df["lat"].median(),
                                             lon = sta_df["lon"].median()
                                             )
                               )
                    )

            
fig=go.Figure(data = [scatt], layout = layout)
plot(fig)