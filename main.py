from selenium import webdriver 
import pandas as pd


inp_url = "https://www.property24.com/for-sale/durban/kwazulu-natal/169"
chrome_path = ('C:/Program Files/Google/Chrome/Driver/chromedriver.exe')

driver = webdriver.Chrome(chrome_path)

driver.get(inp_url)

main_content = driver.find_elements_by_class_name('p24_content')

#basket = ["apple","pear","grape"]

#for index, fruit in enumerate(basket):
#    print(index)
#    print(fruit)
#    if index == 0:
#        basket_record = fruit_record.copy() #initiate the master table
#    else:
#merging the record to the master table
#        basket_record = pd.concat([basket_record, fruit_record], axis = 0, ignore_index=True)
 
    
 
for info in main_content:    
    info = main_content[0].text
    price = info.find_elements_by_class_name('p24_price')[0].text
    prop_title = info.find_elements_by_class_name('p24_title')[0].text
    location = info.find_elements_by_class_name("p24_location")[0].text
    description = info.find_elements_by_class_name("p24_excerpt")[0].text
    feature_details = info.find_elements_by_class_name("p24_featureDetails")[0].text
    main_rec = pd.DataFrame(data =[[price, prop_title, location, description, feature_details]], columns = ["Price", "Title", "Location", "Description", "Feature Deatails"]) 
print(info.text)
 
#Takes me to page 2, need to create a while loop to loop to the end of pages 
driver.find_element_by_xpath("/html/body/div[1]/div[9]/div/div/div[1]/div[5]/div/ul/li[2]/a").click()
 
#needs to be fixed
record = pd.DataFrame(data = [[price, prop_title, location, description, feature_details]], columns = ["Price", "Title", "Location", "Description", "Feature Deatails"])


features = info.find_elements_by_class_name("p24_icons")
feature = features.find_elements_by_class_name("p24_size")
feature = features[0]


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


