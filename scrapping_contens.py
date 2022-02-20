import pandas as pd
import numpy as np
from selenium import webdriver
links = pd.read_csv("address.csv",header=0)
count = 0
medical_reports = [""]*len(links)
keywords = [""]*len(links)
driver = webdriver.Firefox()
for link in links['address'] :
    driver.get(link)
    full_text = driver.find_element_by_class_name("hilightBold").text
    _,result = full_text.split("\n(Medical Transcription Sample Report)\n")
    medical_report, keyword= result.split("Keywords: ")
    medical_report = medical_report[:medical_report.rfind('\n\n')]
    keyword = keyword[:-1]
    medical_reports[count] = medical_report
    keywords[count] = keyword
    count += 1
    links['medical report'] = medical_reports
    links['keyword'] = keywords
    links.to_csv("general_medicine_mtsamples.csv",index=False)
