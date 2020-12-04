def get_address(inp_df):
#     #raw.to_csv("test.csv")
    from geopy.geocoders import Nominatim
    import pandas
#source: https://towardsdatascience.com/geocode-with-python-161ec1e62b89
    
#unit test
locator = Nominatim(user_agent="myGeocoder")
#read data
from pathlib import Path
import os
    
root_dir = Path(__file__).resolve().parent
raw_file = os.path.join(root_dir, 'Address.csv')
raw_df = pandas.read_csv("Address.csv")  
raw_df["Address"] = raw_df["Address"] + " Durban"
raw_df["Address"].loc[(raw_df["Address"] == "unknown")] = raw_df["Location"] + " Durban"
    
# get lon lat via openstreet map - takes about 40mins for 5k records
raw_df["lat"] = ""
raw_df["lon"] = ""
logging.info("getting coordinates")
for index, row in raw_df.iterrows():
    try:
        location = locator.geocode(raw_df["address2"].iloc[index])
        raw_df["lat"][index] = location.latitude
        raw_df["lon"][index] = location.longitude
    except:
            logging.info("failed getting coordinates for " + str(raw_df["address2"].iloc[index]) + " row " + str(index))            
   
        

# MY VERSION

# import pandas, os
# df1 = pandas.read_csv("Address.csv")

# from geopy.geocoders import Nominatim
# Nominatim(user_agent="myGeocoder")
# nom = Nominatim()

# n = nom.geocode("London eye")
# print(n.latitude)

# df1["Address"]=df1["Address"].apply()



# # df1["Latitude"]=df1["Coordinates"].apply(lambda x: x,latitude if x != None else None)
# # df1["Longitude"]=df1["Coordinates"].apply(lambda x: x,longitude if x != None else None)



















