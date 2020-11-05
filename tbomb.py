from selenium import webdriver 
import pandas as pd

inp_url = "https://www.property24.com/for-sale/durban/kwazulu-natal/169"
chrome_path = ('C:/Program Files/Google/Chrome/Driver/chromedriver.exe')

driver = webdriver.Chrome(chrome_path)

driver.get(inp_url)

main_content = driver.find_elements_by_class_name('p24_content')

for index, info in enumerate(main_content):    
    info = main_content[index]
    price = info.find_element_by_class_name('p24_price').text
    prop_title = info.find_elements_by_class_name('p24_title')
    if len(prop_title) > 0:
        prop_title = info.find_elements_by_class_name('p24_title')[0].text
        location = info.find_elements_by_class_name("p24_location")[0].text
        description = info.find_elements_by_class_name("p24_excerpt")[0].text
        
        feature_details = info.find_elements_by_class_name("p24_featureDetails")[0].text
        main_rec = pd.DataFrame(data =[[price, prop_title, location, description, feature_details]], columns = ["Price", "Title", "Location", "Description", "Feature Deatails"]) 

print(info.text)

y = info.text
z = [list(line) for line in y.splitlines()]

x = y.splitlines(True)


