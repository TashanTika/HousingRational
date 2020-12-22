#Read CSV File
import pandas as pd 
import config_p24

address = pd.read_excel(config_p24.all_records_export_path) 

#clean address: 1 - put location for no address
address.loc[(address["Address"] == "No Address"),"Address"] = address.loc[(address["Address"] == "No Address"),"Location"]

#clean address: 2 - remove nan address
address = address.loc[~(address["Address"].isna())]
address.reset_index(drop = True, inplace = True)

address2 = address.iloc[:1000].copy()


#Iterate through the rows to get address
from geopy.geocoders import Nominatim
locator = Nominatim(user_agent="myGeocoder")
location = locator.geocode("Address") 
address2["lat"] = ""
address2["lon"] = ""
for index, row in address2.iterrows():
    print("get location for {}, index {}".format(address["Address"].iloc[index],str(index)))
    location = locator.geocode(address2["Address"].iloc[index] + ", Durban, South Africa")
    # establish if location is none type location == NoneType --> True
    if location == None:
        address2["lon"][index] = float("NaN")
        address2["lat"][index] = float("NaN")
    else:
        address2["lat"][index] = location.latitude
        address2["lon"][index] = location.longitude
        
address2 = address2.loc[~(address2["lon"].isna())]      

#Save file 
address2.to_excel(config_p24.coordinates)

#Links https://towardsdatascience.com/geocode-with-python-161ec1e62b89
      