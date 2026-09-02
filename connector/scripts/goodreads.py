import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

url = 'https://www.goodreads.com/book/show/197744307-underdogs-of-japanese-history'
br = webdriver.Chrome()
br.get(url)
br.find_element( By.CSS_SELECTOR, "button[aria-label='Book details and editions'" ).click()

so = BeautifulSoup( br.page_source, 'html.parser' )

title = so.find( 'h1', attrs={'data-testid': 'bookTitle'} )

rr=so.find_all( 'div', class_ = 'ContributorLinksList' )
for author in rr:
    name = author.find('a').text
    linkAuth = author.find('a')['href']
    display( f"{author}: {linkAuth}" )

description = so.find( 'div', class_ = 'TruncatedContent' ).text

for id in so.find(  'div', class_ = 'FeaturedDetails' ).find_all( 'p' ):
    display( f"{id['data-testid']}: {id.text}" )
    
for dl in so.find( 'dl', class_ = 'DescList' ).find_all( 'div', class_ = 'DescListItem' ):
    ff = dl.find( 'dt' )
    fd = dl.find( 'dd' )
    display( f"{ff.text}: {fd.text}" )
     
