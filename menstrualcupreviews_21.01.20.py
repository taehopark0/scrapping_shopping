import urllib
from bs4 import BeautifulSoup
import os
from selenium import webdriver

URL = 'https://menstrualcupreviews.net/comparison/?show_limit=4&rate=2&cervix=0&capacity=0&shape=0&material=0&made=0&fda=0&firmness=0&brand=0'
xls_save_path = '/Users/taehopark/PycharmProjects/dalchaebi/Naver Crawling/Scrapping/scrapping_shopping'


try:
    if not(os.path.isdir(xls_save_path)):
        os.makedirs(os.path.join(xls_save_path))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Failed to create directory!!!!!")
        raise

driver = webdriver.Chrome('/Users/taehopark/PycharmProjects/dalchaebi/Naver Crawling/Scrapping/chromedriver')
driver.get(URL)
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

driver.get(URL)
product_html = driver.page_source
product_soup = BeautifulSoup(product_html, 'html.parser')

# Extracting other info
pdt_name = product_soup.findAll('div', {'class': 'comparison_row_of_model'})  # 상품 이름


for i in range(len(pdt_name)):
    # image link
    image_html = pdt_name[i].find('div', {'class': 'comparison_data_intro_image'})
    pdt_image_scrap = image_html.find('img')['src']
    print(pdt_image_scrap, i)

    # name
    name = pdt_name[i].find('div', {'class': 'comparison_data comparison_data_cup_name'}).contents[0].replace('\"', '')
    size = pdt_name[i].find('div', {'class': 'comparison_size_tag'}).get_text().replace('/', '')

    name_size = name + ' ' + size
    print(name, '::', size)
    print(name_size)

    # image save
    urllib.request.urlretrieve(pdt_image_scrap, xls_save_path + name_size + '.PNG')