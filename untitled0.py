
def get_address(inp_df):

    from geopy.geocoders import Nominatim
    import pandas
    import logging
    import config_24
    #source: https://towardsdatascience.com/geocode-with-python-161ec1e62b89
    
    #unit test
    locator = Nominatim(user_agent="myGeocoder")
    
    #read data    
    root_dir = Path(__file__).resolve().parent
    raw_file = os.path.join(root_dir, 'Address.csv')
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
       
        raw_df.to_excel(r'C:\Users\Tashan Tika\Desktop\All Rec\coordinates.xlsx')
        get_address(inp_df= raw_df)
        
#Read CSV File
import pandas as pd 
import config_p24

address = pd.read_excel(config_p24.all_records_export_path) 
address2 = address.loc[(address["Address"] != "No Address")]
address3 = address2.loc[~(address2["Address"].isna())]


#Iterate through the rows to get address
from geopy.geocoders import Nominatim
locator = Nominatim(user_agent="myGeocoder")
location = locator.geocode("Champ de Mars, Paris, France")

sample_address2 = address3["Address"].iloc[0] + ", Durban, South Africa"
location2 = locator.geocode(sample_address2)
 
#geopy to find coordinates 
#save file        