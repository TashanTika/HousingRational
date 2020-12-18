# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 18:24:56 2020

@author: neera
"""

# 1 import coordinates
import config_p24
import pandas as pd
raw_df = pd.read_excel(config_p24.coordinates)

# clean all float columns - from string to float
df = raw_df.copy()

df['Price'] = df['Price'].str.replace(" ", "")
df['Price'] = df['Price'].str.replace("R", "")
df['Price'] = df['Price'].str.replace("POA", "NaN")
df['Price'] = df['Price'].astype(float)

# clean size
df["Size"] = df["Size"].str.replace("m²", "")
df["Size"] = df["Size"].str.replace("ha", "")
df["Size"] = df["Size"].str.replace(" ", "")
df['Size'] = df['Size'].astype(float)

# addition cals
df["Price per m²"] = df["Price"] / df["Size"]

# export
df.to_excel(config_p24.dash_ready)