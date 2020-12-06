
import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

ua = UserAgent()
URL = "https://search.shopping.naver.com/search/all?frm=NVSHAKW&origQuery=생리대&pagingIndex=1&pagingSize=40&productSet=total&query=생리대&sort=rel&timestamp=&viewType=list"
headers = {'User-Agent':ua.random}
headline_list =[]
title_list=[]
price_list=[]
type_list=[]

driver = webdriver.Chrome("/Users/taehopark/PycharmProjects/dalchaebi/Naver Crawling/Naver Shopping/chromedriver")


URL1=requests.get(URL)
URL2=BeautifulSoup(URL1.text,'html.parser')

pages_number = URL2.find_all('a',{'class':'pagination_btn_page__FuJaU'})

product_link_list = []
split = URL.split('1')
for i in range(len(pages_number)):
    product_link_list.append(split[0] + str(i) + '&pagingSize=40&productSet=total&query=생리대&sort=rel&timestamp=&viewType=list')
assert len(product_link_list)!=0, "product list is empty"

print(len(product_link_list))

n=1
for i in range(len(product_link_list)):
    driver.get(product_link_list[i])

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

    boxes = driver.find_elements_by_css_selector(".basicList_info_area__17Xyo")
    for j in range(len(boxes)):
        title_list.append(boxes[j].find_element_by_css_selector(".basicList_link__1MaTN").get_attribute("title"))
        price_list.append(boxes[j].find_element_by_css_selector(".price_num__2WUXn").text)
        type_list.append(boxes[j].find_element_by_css_selector(".basicList_desc__2-tko").text)

    driver.find_element_by_css_selector(".pagination_btn_page__FuJaU").click()
    n+=1

df = pd.DataFrame({"title": title_list, "price": price_list, "type&size":type_list})
df.to_excel("result_scrapping_navershopping.xlsx", index=False)