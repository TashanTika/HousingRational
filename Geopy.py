# MY VERSION

import pandas
df = pandas.read_csv("Address.csv")

from geopy.geocoders import Nominatim
Nominatim(user_agent="myGeocoder")
nom = Nominatim()

n = nom.geocode()
print(n.latitude)

df["Address"]=df["Address"].apply()



df["Latitude"]=df["Coordinates"]
df["Longitude"]=df["Coordinates"]