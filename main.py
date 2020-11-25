from selenium import webdriver 
import pandas as pd

inp_url = "https://www.property24.com/for-sale/durban/kwazulu-natal/169"
chrome_path = ('C:/Program Files/Google/Chrome/Driver/chromedriver.exe')

driver = webdriver.Chrome(chrome_path)

driver.get(inp_url)



# this should be a function - scrape page
def scrape(inp_driver):
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
            loop_rec = pd.DataFrame(data = [[price, prop_title, location, description]], 
                            columns = ["Price", "Title", "Location", "Description"]) 

            if len(info.find_elements_by_class_name("p24_icons")) > 0:                
                if len(info.find_elements_by_class_name("p24_size")) > 0:
                    size = info.find_elements_by_class_name("p24_size")
                    loop_rec["size"] = size[0].text

                #loop details                
                details = info.find_elements_by_class_name("p24_featureDetails")
                for detail in details:
                    title = detail.get_attribute("title")
                    value = detail.text
                    loop_rec[title] = value
                    print(title + ":" + value) 

            else:
                icons = 0
            # adjust loop_rec to add feature details 

            if counter == 1:  
                master_rec = loop_rec.copy()
            else: 
                master_rec = pd.concat([master_rec, loop_rec], axis = 0, ignore_index=True)
    return master_rec



page_counter = 0
finish_scraping = False
while finish_scraping == False: 

    #go to a page - make a page loop
    page_counter += 1
    print("--------------scraping page:" + str(page_counter) + "--------------")

    #scrape page
    page_records = scrape(inp_driver = driver)

    #add to all_records
    if page_counter == 1:  
        all_records = page_records.copy()
    else: 
        all_records = pd.concat([all_records, page_records], axis = 0, ignore_index=True)
    print("--------------finished scrape page:" + str(page_counter) + "--------------")
    
    
    #go to next page
    try:
        for i in page_counter:
             xpath = "/html/body/div[1]/div[9]/div/div/div[1]/div[6]/div/ul/li[{0}]/a".format(i)
             driver.find_elements_by_xpath(xpath).click()
    except:
        finish_scraping = True
        
        
        
        
     
        
        
        
        
        
        