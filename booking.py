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


class Booking(Scraping):
    def __init__(self, url: str):
        super().__init__(in_background=False, url=url)

    def extract(self):

        reviews = []

        try:
            review_btn = self.driver.find_element(By.XPATH, "//a[@data-target='hp-reviews-sliding']")

            if review_btn:
                self.driver.execute_script("arguments[0].click();", review_btn)
                time.sleep(5)

        except Exception as e:
            print(e)

        page = self.driver.page_source

        soupe = BeautifulSoup(page, 'lxml')

        # review_c = soupe.find('div', {'id': 'review_list_score_container'})

        review_cards = soupe.find_all('div', {'itemprop': 'review'})
        for card in review_cards:
            title = card.find('h3', {'class': 'c-review-block__title'}).text.strip() if card.find('h3', {'class': 'c-review-block__title'}) else ""
            detail = card.find('span', {'class': 'c-review__body'}).text.strip().replace('\n', ' ') if card.find('span', {'class': 'c-review__body'}) else ""
            comment = f"{title}{': ' if title and detail else ''}{detail}"

            try:
                lang = detect(comment)
            except: 
                lang = 'en'

            try:
                reviews.append({
                    'comment': comment,
                    'rating': card.find('div', {'class': 'bui-review-score__badge'}).text.strip() \
                                if card.find('div', {'class': 'bui-review-score__badge'}) else "0",
                    'language': lang,
                    'source': urlparse(self.url).netloc.split('.')[1],
                    'author': card.find('span', {'class': 'bui-avatar-block__title'}).text.strip() if card.find('span', {'class': 'bui-avatar-block__title'}) else "",
                    'establishment': '/api/establishments/2'
                })
            except Exception as e:
                print(e)
                continue

        self.data = reviews


trp = Booking(url="https://www.booking.com/hotel/fr/ha-tel-le-christiania.fr.html")
trp.execute()
# print(trp.data)