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


class Trustpilot(Scraping):
    def __init__(self, url: str):
        super().__init__(in_background=False, url=url)

    def extract(self):

        page = self.driver.page_source

        soupe = BeautifulSoup(page, 'lxml')

        reviews = []

        review_cards = soupe.find_all('article', {'data-service-review-card-paper': "true"})
        for card in review_cards:
            title = card.find('a', {'data-review-title-typography': 'true'}).text.strip() if card.find('a', {'data-review-title-typography': 'true'}) else ""
            detail = card.find('p', {'data-service-review-text-typography': 'true'}).text.strip() if card.find('p', {'data-service-review-text-typography': 'true'}) else ""
            comment = f"{title}{': ' if title and detail else ''}{detail}"

            try:
                lang = detect(comment)
            except: 
                lang = 'en'

            reviews.append({
                'comment': comment,
                'rating': card.find('div', {'data-service-review-rating': True})['data-service-review-rating'] if card.find('div', {'data-service-review-rating': True}) else "0",
                'language': lang,
                'source': urlparse(self.url).netloc.split('.')[1],
                'author': card.find('span', {'data-consumer-name-typography': 'true'}).text.strip() if card.find('span', {'data-consumer-name-typography': 'true'}) else "",
                'establishment': '/api/establishments/4'
            })

        self.data = reviews


trp = Trustpilot(url="https://fr.trustpilot.com/review/liberkeys.com")
trp.execute()
# print(trp.data)