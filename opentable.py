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


class OpenTable(Scraping):
    def __init__(self, in_background: bool = False, url: str = None):
        super().__init__(in_background=in_background, url=url)

    def extract(self):
        def find_detail(data_test):
            value = ''
            if soupe.find('span', {"data-test": data_test}):
                if soupe.find('span', {"data-test": data_test}).parent.find('p'):
                    value = soupe.find('span', {"data-test": data_test}).parent.find('p').text.strip()
                elif soupe.find('span', {"data-test": data_test}).parent.find('div') and soupe.find('span', {"data-test": data_test}).parent.find('div').find('p'):
                    value = soupe.find('span', {"data-test": data_test}).parent.find('div').find('p').text.strip()
                else:
                    value = soupe.find('span', {"data-test": data_test}).parent.text.strip()
            return value

        page = self.driver.page_source

        soupe = BeautifulSoup(page, 'lxml')

        page_content = soupe.find('div', {"data-test": "restaurant-banner"}).parent

        name = page_content.find('h1').text.strip()

        url = self.driver.current_url

        resume = page_content.find('div', {"data-test": "restaurant-overview-header"})

        stars = resume.find('div', {'id': 'ratingInfo'}).find('span').text.strip() if resume.find('div', {'id': 'ratingInfo'}) else '0'

        review_count = int(resume.find('div', {'id': 'reviewInfo'}).text.strip().split(' ')[0]) if resume.find('div', {'id': 'reviewInfo'}).text.strip().split(' ')[0] != 'No' else 0

        phone = find_detail('icPhone')

        locality = find_detail('icLocation')

        open_state =  find_detail('icClock').split('\n')

        website = find_detail('icNewWindow')

        reviews = []
        reviews_list = []
        if soupe.find('section', {'id':'reviews'}) and soupe.find('section', {'id':'reviews'}).find('ol',{'data-test': 'reviews-list'}):
            reviews_list = soupe.find('section', {'id':'reviews'}).find('ol',{'data-test': 'reviews-list'}).find_all('li')

        for item in reviews_list:
            review = {}
            review['comment'] = item.find('span', {'data-test':'wrapper-tag'}).text.strip()
            review['rating'] = item.find_all('section')[1].find_all('section')[0].find_all('div')[0].text.strip()
            try:
                review['language'] = detect(review['comment'])
            except:
                review['language'] = 'en'
            review['source'] = urlparse(url).netloc.split('.')[1]
            # review['reviewsTime'] = item.find_all('section')[1].find_all('section')[0].find_all('p')[-1].text.strip()
            review['author'] = ', '.join([item.find_all('section')[0].find_all('p')[0].text.strip(), item.find_all('section')[0].find_all('p')[1].text.strip()])
            review['establishment'] = '/api/establishments/2'
            reviews.append(review)

        # data = {}
        # data['name'] = name
        # data['rating'] = stars
        # data['reservable'] = ''
        # data['url'] = url
        # data['addressComponentsLongName'] = locality
        # data['website'] = website
        # data['takeout'] = True
        # data['internationalPhoneNumber'] = phone
        # data['userRatingsTotal'] = review_count
        # data['utcOffset'] = 0
        # data['wheelchairAccessibleEntrance'] = True
        # data['reviews'] = reviews

        self.data = reviews


# trp = OpenTable()
# trp.set_url("https://www.opentable.com/r/chatkar-beau-champ")
# trp.execute()
# print(trp.data)