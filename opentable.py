from scraping import Scraping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from abc import abstractmethod
import sys
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from langdetect import detect


class OpenTable(Scraping):
    def __init__(self, in_background: bool = False, url: str = None):
        super().__init__(in_background=in_background, url=url)

    def extract(self):
        page = self.driver.page_source

        soupe = BeautifulSoup(page, 'lxml')

        reviews = []
        reviews_list = []
        if soupe.find('section', {'id':'reviews'}) and soupe.find('section', {'id':'reviews'}).find('ol',{'data-test': 'reviews-list'}):
            reviews_list = soupe.find('section', {'id':'reviews'}).find('ol',{'data-test': 'reviews-list'}).find_all('li')

        for item in reviews_list:
            
            comment = item.find('span', {'data-test':'wrapper-tag'}).text.strip() if item.find('span', {'data-test':'wrapper-tag'}) else ""

            try:
                lang = detect(comment)
            except:
                lang = 'en'

            reviews.append({
                'comment': comment,
                'language': lang,
                'rating': item.find_all('section')[1].find_all('section')[0].find_all('div')[0].text.strip() if item.find_all('section')[1] and item.find_all('section')[1].find_all('section')[0].find_all('div')[0] else "0",
                'source': urlparse(self.url).netloc.split('.')[1],
                'author': ', '.join([item.find_all('section')[0].find_all('p')[0].text.strip(), item.find_all('section')[0].find_all('p')[1].text.strip()]),
                'establishment': '/api/establishments/2'
            })

        self.data = reviews


trp = OpenTable()
trp.set_url("https://www.opentable.com/r/chatkar-beau-champ")
trp.execute()
# print(trp.data)