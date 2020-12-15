# MY VERSION

import pandas
df = pandas.read_csv("Address")

from geopy.geocoders import Nominatim
Nominatim(user_agent="myGeocoder")
nom = Nominatim()

n = nom.geocode()
print(n.latitude)

df["Address"]=df["Address"].apply()

print(" test commit" )

df["Latitude"]=df["Coordinates"]
df["Longitude"]=df["Coordinates"]

# Original 
def get_address(inp_df):

    from geopy.geocoders import Nominatim
    import pandas
    import logging
    #source: https://towardsdatascience.com/geocode-with-python-161ec1e62b89
    
    #unit test
    locator = Nominatim(user_agent="myGeocoder")
#read data

        
# root_dir = Path(__file__).resolve().parent
# raw_file = os.path.join(root_dir, 'Address.csv')
    raw_df = pandas.read_csv("Address.csv")  
    raw_df["Address"] = raw_df["Address"] + " Durban"
    raw_df["Address"].loc[(raw_df["Address"] == " ")] = raw_df["Location"] + " Durban"
    
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