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


class Tripadvisor(Scraping):
    def __init__(self, in_background: bool = False, url: str = None):
        super().__init__(in_background=in_background, url=url)

    def extract(self):
        try:
            page = self.driver.page_source

            soupe = BeautifulSoup(page, 'lxml')

            reviews_card = soupe.find_all('div', {'data-test-target':"HR_CC_CARD"})
            reviews = []
            print(len(reviews_card))

            for item in reviews_card:
                # try:
                #     review['reviewLangage'] = detect(review['reviewsText'])
                # except:
                #     print("Erreur langue: ", review['reviewsText'])
                #     review['reviewLangage'] = 'en'
                title = item.find('div', {'data-test-target':'review-title'}).text.strip() if item.find('div', {'data-test-target':'review-title'}) else ''
                detail = item.find('span', {'class':'QewHA'}).find('span').text.strip().replace('\n', '') if item.find('span', {'class':'QewHA'}) else ''
                comment = f"{title}{': ' if title and detail else ''}{detail}"
                
                try:
                    lang = detect(comment)
                except:
                    lang = 'en'

                reviews.append({
                    'comment': comment,
                    'rating': str(int(item.find('span', class_='ui_bubble_rating')['class'][1].split('_')[1]) / 10) if item.find('span', class_='ui_bubble_rating') else "0",
                    'language': lang,
                    'source': urlparse(self.url).netloc.split('.')[1],
                    'author': item.find('a', class_='ui_header_link').text.strip() if item.find('a', class_='ui_header_link') else "",
                    'establishment': '/api/establishments/4'
                })

            self.data = reviews

        except Exception as e:
            print("erreur:", e)


trp = Tripadvisor(url="https://www.tripadvisor.fr/Hotel_Review-g1056032-d1055274-Reviews-Madame_Vacances_Les_Chalets_de_Berger-La_Feclaz_Savoie_Auvergne_Rhone_Alpes.html")
trp.execute()
# print(trp.data)