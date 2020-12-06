import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

ua = UserAgent()
URL = []
url = "https://search.shopping.naver.com/search/all?query=생리대&cat_id=&frm=NVSHAKW"
headers = {'User-Agent':ua.random}
headline_list =[]

driver = webdriver.Chrome("/Users/taehopark/PycharmProjects/dalchaebi/Naver Crawling/Naver Shopping/chromedriver")
driver.get("https://search.shopping.naver.com/search/all?query=생리대&cat_id=&frm=NVSHAKW")

SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
title_list=[]
price_list=[]
type_list=[]
boxes = driver.find_elements_by_css_selector(".basicList_info_area__17Xyo")
for i in range(len(boxes)):
    title_list.append(boxes[i].find_element_by_css_selector(".basicList_link__1MaTN").get_attribute("title"))
    price_list.append(boxes[i].find_element_by_css_selector(".price_num__2WUXn").text)
    type_list.append(boxes[i].find_element_by_css_selector(".basicList_desc__2-tko").text)

df = pd.DataFrame({"title": title_list, "price": price_list, "type&size":type_list})
df.to_excel("navershopping_20201129.xlsx", index=False)



