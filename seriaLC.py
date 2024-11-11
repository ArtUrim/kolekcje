# coding: utf-8
url = 'https://lubimyczytac.pl/cykl/5256/kajko-i-kokosz'
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
br = webdriver.Chrome()
br.get(url)
so = BeautifulSoup( br.page_source, 'html.parser' )

bb=so.find_all( 'a', class_ = 'authorAllBooks__singleTextTitle' )
bb[0]['href']
bb[0].text

    
try:
    br.find_element( By.CLASS_NAME, 'icon-arrow-next').click()
except Exception as e:
    display(e)
    
