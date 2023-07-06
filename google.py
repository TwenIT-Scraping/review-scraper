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


class Google(Scraping):
    def __init__(self, url: str):
        super().__init__(in_background=False, url=url)

    def extract(self):

        # review_btn = self.driver.find_element(By.XPATH, "//div[@data-tab='reviews']/button")
        # print(review_btn)

        time.sleep(5)

        reviews = []

        # try:
        #     plus_btns = self.driver.find_elements(By.XPATH, "//span[@jsname='kDNJsb']")

        #     if len(plus_btns):
        #         for btn in plus_btns:
        #             print("click ...")
        #             self.driver.execute_script("arguments[0].click();", btn)
        #             time.sleep(2)

        # except Exception as e:
        #     print(e)

        page = self.driver.page_source

        soupe = BeautifulSoup(page, 'lxml')

        review_container = soupe.find_all('div', {'jsname': "Pa5DKe"})

        for container in review_container:
            cards = container.find_all('div', {'data-hveid': True})
            for card in cards:
                author = card.find('span', {'class': 'k5TI0'}).find('a').text.strip() if card.find('span', {'class': 'k5TI0'}) and card.find('span', {'class': 'k5TI0'}).find('a') else ""
                comment = card.find('div', {'class': 'K7oBsc'}).text.strip().replace(" En savoir plus", "") if card.find('div', {'class': 'K7oBsc'}) else ""
                rating = card.find('div', {'class': 'GDWaad'}).text.strip().split('/')[0] if card.find('div', {'class': 'GDWaad'}) else "0"

                try:
                    lang = detect(comment)
                except: 
                    lang = 'en'

                if author or comment or rating != "0":

                    reviews.append({
                        'rating': rating,
                        'author': author,
                        'comment': comment,
                        'language': lang,
                        'source': urlparse(self.url).netloc.split('.')[1],
                        'establishment': '/api/establishments/4'
                    })

        # for card in review_cards:
        #     title = card.find('a', {'data-review-title-typography': 'true'}).text.strip() if card.find('a', {'data-review-title-typography': 'true'}) else ""
        #     detail = card.find('p', {'data-service-review-text-typography': 'true'}).text.strip() if card.find('p', {'data-service-review-text-typography': 'true'}) else ""
        #     comment = f"{title}{': ' if title and detail else ''}{detail}"

        

        #     reviews.append({
        #         'comment': comment,
        #         'rating': card.find('div', {'data-service-review-rating': True})['data-service-review-rating'] if card.find('div', {'data-service-review-rating': True}) else "0",
        #         'language': lang,
        #         'source': urlparse(self.url).netloc.split('.')[1],
        #         'author': card.find('span', {'data-consumer-name-typography': 'true'}).text.strip() if card.find('span', {'data-consumer-name-typography': 'true'}) else "",
        #         'establishment': '/api/establishments/4'
        #     })

        self.data = reviews


trp = Google(url="https://www.google.fr/travel/search?q=les%20balcons%20d%27aix&g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4597339%2C4754388%2C4757164%2C4814050%2C4850738%2C4864715%2C4874190%2C4886480%2C4893075%2C4924070%2C4965990%2C4985712%2C4990494%2C72248281%2C72254381%2C72271797%2C72276651%2C72279098%2C72281254&hl=fr-FR&gl=fr&ssta=1&ts=CAESABpJCikSJzIlMHg0NzhiYTQyNmFjZTRmY2VmOjB4YjI1OTUyNmUzODQ2NTdhMxIcEhQKBwjnDxAGGBsSBwjnDxAGGBwYATIECAAQACoHCgU6A01HQQ&qs=CAEyJkNoZ0lvNi1ad3VQTjFLeXlBUm9MTDJjdk1YUjNYMjB6Y1hFUUFROAJCCwmjV0Y4blJZshgBQgsJo1dGOG5SWbIYAQ&ap=ugEHcmV2aWV3cw&ictx=1&sa=X")
trp.execute()
# print(trp.data)