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
import plotly.express as px
from plotly.offline import plot
px.set_mapbox_access_token(conf.mapbox_token)
fig = px.scatter_mapbox(sta_df,
                        lat = "lat",
                        lon = "lon",
                        )
fig.show()
plot(fig)