# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 17:11:01 2020
@author: Tashan Tika
"""

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


def extract_p24():
    from selenium import webdriver 
    import pandas as pd
    
    inp_url = "https://www.property24.com/for-sale/durban/kwazulu-natal/169"
    chrome_path = ('C:/Program Files/Google/Chrome/Driver/chromedriver.exe')
    
    driver = webdriver.Chrome(chrome_path)
    driver.get(inp_url)
    
    for page_counter in range(250):  
        print("--------------scraping page:" + str(page_counter +1) + "--------------")
        
        href = "https://www.property24.com/for-sale/durban/kwazulu-natal/169/p{0}".format(page_counter+1)    
        driver.get(href)
        page_records = scrape(inp_driver = driver)
        
        #add to all_records
        if page_counter == 0:  
            all_records = page_records.copy()
        else: 
            all_records = pd.concat([all_records, page_records], axis = 0, ignore_index=True)
        print("--------------finished scrape page:" + str(page_counter + 1) + "--------------")
                
        
    #To export to CSV file in desktop     
    all_records.to_excel (r'C:\Users\Tashan Tika\Desktop\All Rec\All Records.xlsx')


               
        
        
        
        
        
        
        
        