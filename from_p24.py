# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 19:43:01 2020

@author: Tashan Tika
"""

#extract
def scrape(inp_driver):
    import pandas as pd
    main_class = inp_driver.find_elements_by_class_name('p24_content')
    counter = 0
    for index, info in enumerate(main_class):  
        print_info = main_class[index].text
        print(print_info)    

        info = main_class[index]
        if len(info.find_elements_by_class_name('p24_information')) > 0 or len(info.find_elements_by_class_name('p24_schema')) > 0:
            p24_add = True
            print("-----" + str(index) + " is an add -------")
        else:
           p24_add = False
           counter = counter + 1

        if p24_add == False:
            price = info.find_elements_by_class_name('p24_price')[0].text
            prop_title = info.find_elements_by_class_name('p24_title')[0].text
            location = info.find_elements_by_class_name("p24_location")[0].text
            description = info.find_elements_by_class_name("p24_excerpt")[0].text
            #Trying to add address 
            if len(info.find_elements_by_class_name("p24_address")) > 0:
                address = info.find_elements_by_class_name("p24_address")[0].text
            else:
                address = "No Address"
                
                
                #do not change from here 
            loop_rec = pd.DataFrame(data = [[price.format(int()), prop_title, location, description, address,]], 
                            columns = ["Price", "Title", "Location", "Description", "Address",]) 
            
            if len(info.find_elements_by_class_name("p24_icons")) > 0:                
                if len(info.find_elements_by_class_name("p24_size")) > 0:
                    size = info.find_elements_by_class_name("p24_size")
                    loop_rec["Size"] = size[0].text

                #loop details                
                details = info.find_elements_by_class_name("p24_featureDetails")
                for detail in details:
                    title = detail.get_attribute("title")
                    value = detail.text
                    loop_rec[title] = value
                    print(title + ":" + value) 
                
                # Getting Links For Each Individual Lisiting 
                all_links = inp_driver.find_elements_by_xpath("//*[contains(@class, 'p24_regularTile js_rollover_container')]")
                index_link_main = all_links[index]
                index_link_a = index_link_main.find_elements_by_tag_name("a")
                web_elem = index_link_a[0].get_attribute("href")
                loop_rec["Link"] = web_elem
                print(web_elem)   
               

            else:
                icons = 0
            # adjust loop_rec to add feature details 

            if counter == 1:  
                master_rec = loop_rec.copy()
            else: 
                master_rec = pd.concat([master_rec, loop_rec], axis = 0, ignore_index=True)
    return master_rec

def extract_p24(**kwargs):
    from selenium import webdriver 
    import pandas as pd
    import config_p24
    
    inp_url = config_p24.inp_url
    chrome_path = config_p24.chrome_path 
    inp_last_page = kwargs.get("inp_last_page", None)
    
    driver = webdriver.Chrome(chrome_path)
    driver.get(inp_url)
    
    #find last page
    if inp_last_page == None:
        pager = driver.find_elements_by_class_name("pagination")
        pager = pager[0].find_elements_by_tag_name("li")
        last_page = int(pager[-1].text)
    else:
        last_page = inp_last_page
            
    for page_counter in range(last_page):  
        print("--------------scraping page:" + str(page_counter +1) + "--------------")
        
        href_base = inp_url + "/p{0}"
        href = href_base.format(page_counter+1)    
        driver.get(href)
        page_records = scrape(inp_driver = driver)
        
        #add to all_records
        if page_counter == 0:  
            all_records = page_records.copy()
        else: 
            all_records = pd.concat([all_records, page_records], axis = 0, ignore_index=True)
        print("--------------finished scrape page:" + str(page_counter + 1) + "--------------")
    return all_records

def transform_p24(inp_df):
    print("start transform p24")
    #def transform_p24(inp_df):
    inp_df["filter empty row"] = inp_df["Price"] + inp_df["Title"]  + inp_df["Location"] 
    df = inp_df.loc[(inp_df["filter empty row"] != "")]
    df.loc[(df["Address"] == "No Address"),"Address"] = df.loc[(df["Address"] == "No Address"),"Location"]
    df.reset_index(drop = True, inplace = True)
    
    #Clean Price
    print("start transform price and size")
    df["Price"].loc[(df["Price"] == "")] = "NaN"
    df['Price'] = df['Price'].str.replace(" ", "")
    df['Price'] = df['Price'].str.replace("R", "")
    df['Price'] = df['Price'].str.replace("POA", "NaN")
    df['Price'] = df['Price'].astype(float)
    
    # clean size
    df["Size"] = df["Size"].str.replace("m²", "")
    df["Size"] = df["Size"].str.replace("ha", "")
    df["Size"] = df["Size"].str.replace(" ", "")
    df['Size'] = df['Size'].astype(float)
    
    #Price Per Square meter
    df["Price per m²"] = df["Price"] / df["Size"]
    
    # get lat lon
    print("start transform lat and lon")
    import get_coordinates as gc
    df = gc.get_lat_lon(inp_df = df, 
                         inp_address_column_name = "Address", 
                         inp_city_country_name = "Durban, South Africa")
    
    return df


extract_df = extract_p24(inp_last_page = 2)
transform = transform_p24(inp_df = extract_df)
print("load p24")


# take nans/empty rows
# add an insert date
# add an id


#load - 
# load into sql