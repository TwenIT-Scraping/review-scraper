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


class Expedia(Scraping):
    def __init__(self, url: str):
        super().__init__(in_background=False, url='https://www.expedia.com/Les-Deserts-Hotels-Vacanceole-Les-Balcons-DAix.h2481279.Hotel-Reviews')

    def extract(self):

        page = self.driver.page_source

        soupe = BeautifulSoup(page, 'lxml')

        reviews = []

        review_cards = soupe.find_all('article', {'itemprop': 'review'})
        for card in review_cards:
            reviews.append({
                'comment': """%s: %s""" % (
                    card.find('span', {'itemprop': 'name'}).text.strip() if card.find('span', {'itemprop': 'name'}) else "", 
                    card.find('span', {'itemprop': 'description'}).text.strip() if card.find('span', {'itemprop': 'description'}) else ""),
                'rating': card.find('span', {'itemprop': 'ratingValue'}).text.strip().split('/')[0] \
                            if card.find('span', {'itemprop': 'ratingValue'}) else "",
                'language': 'fr',
                'source': urlparse(url).netloc.split('.')[1],
                'author': card.find('h4').text.strip(),
                'establishment': '/api/establishments/2'
            })
        # reviews_list = []
        # if soupe.find('section', {'id':'reviews'}) and soupe.find('section', {'id':'reviews'}).find('ol',{'data-test': 'reviews-list'}):
        #     reviews_list = soupe.find('section', {'id':'reviews'}).find('ol',{'data-test': 'reviews-list'}).find_all('li')

        # for item in reviews_list:
        #     review = {}
        #     review['comment'] = item.find('span', {'data-test':'wrapper-tag'}).text.strip()
        #     review['rating'] = item.find_all('section')[1].find_all('section')[0].find_all('div')[0].text.strip()
        #     try:
        #         review['language'] = detect(review['comment'])
        #     except:
        #         review['language'] = 'en'
        #     review['source'] = urlparse(url).netloc.split('.')[1]
        #     # review['reviewsTime'] = item.find_all('section')[1].find_all('section')[0].find_all('p')[-1].text.strip()
        #     review['author'] = ', '.join([item.find_all('section')[0].find_all('p')[0].text.strip(), item.find_all('section')[0].find_all('p')[1].text.strip()])
        #     review['establishment'] = '/api/establishments/2'
        #     reviews.append(review)

        self.data = reviews


# trp = OpenTable()
# trp.set_url("https://www.opentable.com/r/chatkar-beau-champ")
# trp.execute()
# print(trp.data)