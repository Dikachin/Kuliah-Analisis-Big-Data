import pandas as pd
import numpy as np
from selenium import webdriver

#run driver selenium
driver = webdriver.Firefox()
driver.get('https://www.mtsamples.com/site/pages/browse.asp?type=98-General%20Medicine')


#ngeclick option button untuk mengubah tampilan menjadi 100 medical record perhalaman
driver.find_element_by_class_name("custom-select").click()
driver.find_element_by_xpath("/html/body/main/div/div/div[2]/div[3]/div/div[1]/div[2]/label/select/option[4]").click()

#proses ambil link setiap medical record
links = []
while True :
    try :
        driver_medical = driver.find_elements_by_class_name("sorting_1")
        for link in driver_medical :
            address = link.find_element_by_tag_name("a").get_attribute("href")
            title,description = link.text.split("\n")
            links.append((title,description, address))
        #save
        result = pd.DataFrame(links,columns=["title","description","address"])
        result.to_csv("address.csv",index=False)
        #pindah page
        driver.find_element_by_xpath("/html/body/main/div/div/div[2]/div[3]/div/div[1]/div[4]/ul/li[5]/a").click()
    except :
        #page sudah habis
        print("Halaman Terakhir")
        break