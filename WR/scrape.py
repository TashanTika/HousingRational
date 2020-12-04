# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 16:26:44 2020
@author: Working Rational
#http://kbroman.org/github_tutorial/pages/fork.html
"""
import logging   
import log_init 
        
def scrape_page(inp_driver):
    from requests import get
    from bs4 import BeautifulSoup 
    import pandas as pd
                   
    record_columns = ["Listing_id","Location","Address", "Price","Title","Agent","Url"]
    datapoints = ['p24_price','p24_location','p24_address','p24_title',"p24_branding js_agencyBrandingLink js_disablePropagation","Url"] #standard columns
    listing_class = "p24_regularTile js_rollover_container"
    listing_id_tag = "data-listing-number"
    
    inp_page_url = inp_driver.current_url
    response = get(inp_page_url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
     
    #need to scrape per listing because feature details are listing dependent
    listings = html_soup.find_all('div', class_ = listing_class)
    
    #create pandas dataframe with dynamic columns 
    for index, listing in enumerate(listings):
        listing_id = listing[listing_id_tag]                
        for datapoint in datapoints:
            item = listing.find_all('span', class_ = datapoint)
            if datapoint == "p24_price":
                try:
                    price = item[0]["content"]
                except:
                    price = item[0].text.strip()
            elif datapoint == "p24_location":
                location = item[0].text
            elif datapoint == "p24_address":
                try:
                    address = item[0].text                  
                except:
                    address = "unknown"
            elif datapoint == "p24_title":
                title = item[0].text  
            elif datapoint == "p24_branding js_agencyBrandingLink js_disablePropagation":
                try:
                    agent = item[0].find_all("meta")[0]["content"]
                except:
                    agent = "unknown"
            elif datapoint == "Url":                
                url = listing.find_all('a')
                url = url[0]["href"]
                                                                
        record = pd.DataFrame([[listing_id, location, address, price, title, agent, url]],columns=record_columns)
        features = listing.find_all('span', class_ = "p24_icons")
        features = features[0].find_all('span') #go through each span and check for title
        for feature in features:
            try:
                record[feature["title"]] = feature.text.strip()
            except:
                pass
        if index == 0:
            records = record.copy()
        else:
            records = pd.concat([records, record], axis = 0, ignore_index = True)
    return records

def scrape_all():
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    import pandas as pd
    from time import sleep
    from random import randrange
    from pathlib import Path
    import os
        
    #step 1. Open website and go to page
    root_dir = Path(__file__).resolve().parent #root directory
    chrome_path = os.path.join(root_dir, 'driver/chromedriver.exe') #download this file from https://sites.google.com/a/chromium.org/chromedriver/downloads    
    inp_url = "https://www.property24.com"
    inp_search = "Durban, KwaZulu Natal"
    id_search = "token-input-AutoCompleteItems"
    xpath_button = "//button[contains(@class, 'btn btn-danger')]"
    xpath_ref = "//a[contains(@title, '" + inp_search + "')]"
    xpath_delay = 3
    xpath_next_page = "//a[@class = 'pull-right']"
 
    #move to results page
    driver = webdriver.Chrome(executable_path=chrome_path)
    driver.get(inp_url)
    try:
        driver.find_element_by_id(id_search).send_keys(inp_search)
    except NoSuchElementException:
        logging.info("maintenance on the website")
    else:        
        driver.find_elements_by_xpath(xpath_button)[0].click()
        try:
            wait_element = WebDriverWait(driver, xpath_delay).until(EC.presence_of_element_located((By.XPATH, xpath_ref)))    
        except TimeoutException:
            logging.info("loading took too much time")
        else:            
            driver.find_elements_by_xpath(xpath_ref)[0].click()
            logging.info("entered results page")
            
            #loop through each result page and scrape            
            passed_page = True
            counter = 0
            while passed_page == True:
                counter += 1       
                page_results = scrape_page(inp_driver = driver) #scrape page
                logging.info("scraped page " + str(counter))
                if counter == 1:
                    all_results = page_results.copy()
                else:
                    all_results = pd.concat([all_results,page_results], axis = 0, ignore_index = True)
                #try to move to the next page
                try:     
                    wait_element = WebDriverWait(driver, xpath_delay).until(EC.presence_of_element_located((By.XPATH, xpath_next_page)))
                    sleep(randrange(2)) #add random sleep to prevent activtation of ddos protection 
                    driver.find_elements_by_xpath(xpath_next_page)[0].click()         
                except TimeoutException:        
                    passed_page = False
                    logging.info("finished page")
            
            logging.info("clean scrape results")
            all_results = clean_scrape(inp_df = all_results)
            all_results = get_address(inp_df = all_results)
            return all_results

def clean_scrape(inp_df):
    import pandas as pd
    from datetime import datetime
    now = datetime.now()
    
    float_columns = ["Price","Bedrooms","Bathrooms","Parking Spaces","Erf Size","Floor Size","Gross Lettable Area"]    
    for column in float_columns:
        try:
            inp_df[column] = inp_df[column].str.replace(" ","")
            inp_df[column] = inp_df[column].str.replace("m²","")           
            inp_df[column] = pd.to_numeric(inp_df[column], errors='coerce')
        except:
            logging.info("clean str to float failed for column " + column)
            
    inp_df["insert_date"] = now
    inp_df["price per m2 Erf"] = inp_df["Price"] / inp_df["Erf Size"] 
    inp_df["price per m2 Floor"] = inp_df["Price"] / inp_df["Floor Size"] 
    return inp_df

def get_address(inp_df):
    #raw.to_csv("test.csv")
    from geopy.geocoders import Nominatim
    import pandas as pd
    #source: https://towardsdatascience.com/geocode-with-python-161ec1e62b89
    
    #unit test
    locator = Nominatim(user_agent="myGeocoder")
    
    #read data
    #from pathlib import Path
    #import os
    
    #root_dir = Path(__file__).resolve().parent
    #raw_file = os.path.join(root_dir, 'latest_scrape.csv')
    #raw_df = pd.read_csv(raw_file)  
    raw_df = inp_df.copy()
    raw_df["address2"] = raw_df["Address"] + " Durban"
    raw_df["address2"].loc[(raw_df["Address"] == "unknown")] = raw_df["Location"] + " Durban"
    
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
    return raw_df
        
# create a catch for missing lon lat via google maps?    
#raw_df.to_csv("osm_cleaned.csv")
"""

def main():
    scrape = scrape_all()
    scrape.to_csv("latest_scrape.csv")

if __name__ == '__main__':
    main()        
    
"""