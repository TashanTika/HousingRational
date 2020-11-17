from selenium import webdriver 
import pandas as pd

inp_url = "https://www.property24.com/for-sale/durban/kwazulu-natal/169"
chrome_path = ('C:/Program Files/Google/Chrome/Driver/chromedriver.exe')

driver = webdriver.Chrome(chrome_path)

driver.get(inp_url)

main_class = driver.find_elements_by_class_name('p24_content')
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
        icons = info.find_element_by_class("p24_featureDetails")[0].text
        for fd in icons:
                icons.getAttribute("title=Bedrooms")
       
        if len(info.find_elements_by_class_name("p24_featureDetails")) > 0:
            #loop through p24 features
            feature_details = info.find_elements_by_class_name("p24_featureDetails")[0].text
        else:
            feature_details = 0
        # adjust loop_rec to add feature details 
        loop_rec = pd.DataFrame(data =[[price, prop_title, location, description, feature_details]], 
                                columns = ["Price", "Title", "Location", "Description", "Feature Deatails"]) 
        if counter == 1:  
            master_rec = loop_rec.copy()
        else: 
            master_rec = pd.concat([master_rec, loop_rec], axis = 0, ignore_index=True)


    
"""    
    for index, info in enumerate(main_class):
        print(index)
        if index == 0:  
            print("copy loop record")
        else:
            print("paste loop record under latest master record")
"""
    
    
    
""" 

for index, info in enumerate(main_class):    
    info = main_class[2].text
    price = info.find_elements_by_class_name('p24_price')[0].text
    prop_title = info.find_elements_by_class_name('p24_title')[0].text
    location = info.find_elements_by_class_name("p24_location")[0].text
    description = info.find_elements_by_class_name("p24_excerpt")[0].text
    feature_details = info.find_elements_by_class_name("p24_featureDetails")[0].text
    
    if index == 0:
        pass
        master_rec = ([price, prop_title, location, description, feature_details]).copy(info_list)
    else: master_rec = pd.concat([info, master_rec], axis = 0, ignore_index=True)
main_rec = pd.DataFrame(data =[[price, prop_title, location, description, feature_details]], columns = ["Price", "Title", "Location", "Description", "Feature Deatails"]) 
print(info.text)
""" 

# =============================================================================
# info_list = [] 
# info_dict = {
#         "price" : price,
#         "title": title,
#         "location": location,
#         "address" : address,
#         "description" : description
#         
#         }
# 
# info_list.append(info_dict)
#    
# df = pd.DataFrame(info_list)
# print(df)
# 
# =============================================================================
