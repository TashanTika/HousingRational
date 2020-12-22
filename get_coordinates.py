# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 20:44:21 2020

@author: Tashan Tika
"""
# inp_df
# inp_address_column_name
# inp_city_country_name
def get_lat_lon(inp_df, inp_address_column_name, inp_city_country_name):
    from geopy.geocoders import Nominatim
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode("Address") 
    inp_df.reset_index(drop = True, inplace = True)
    inp_df["lat"] = ""
    inp_df["lon"] = ""
    for index, row in inp_df.iterrows():
        print("get location for {}, index {}".format(inp_df[inp_address_column_name].iloc[index],str(index)))
        location = locator.geocode(inp_df[inp_address_column_name].iloc[index] + ", " + inp_city_country_name)
        # establish if location is none type location == NoneType --> True
        if location == None:
            inp_df["lon"][index] = float("NaN")
            inp_df["lat"][index] = float("NaN")
        else:
            inp_df["lat"][index] = location.latitude
            inp_df["lon"][index] = location.longitude
            
    inp_df = inp_df.loc[~(inp_df["lon"].isna())]  
    return inp_df