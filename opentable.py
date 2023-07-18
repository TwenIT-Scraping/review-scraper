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
        self.reviews_data = []

    def extract(self):
 
        p = 1

        while True:
            page = self.driver.page_source

            time.sleep(10)

            soupe = BeautifulSoup(page, 'lxml')

            if soupe.find('h3', string='Reviews could not be updated'):
                print("Refresh page")
                self.driver.refresh()
                time.sleep(5)
                self.extract()
            
            reviews_list = []
            if soupe.find('section', {'id':'reviews'}) and soupe.find('section', {'id':'reviews'}).find('ol',{'data-test': 'reviews-list'}):
                reviews_list = soupe.find('section', {'id':'reviews'}).find('ol',{'data-test': 'reviews-list'}).find_all('li')

            ligne = 1

            for item in reviews_list:
                
                comment = item.find('span', {'data-test':'wrapper-tag'}).text.strip() if item.find('span', {'data-test':'wrapper-tag'}) else ""
                By.XPATH, "//button[contains(text(), 'See all reviews')]"
                try:
                    rating_container = item.find('span', string='overall').parent
                    rating_items = rating_container.find_all('span')
                    rating = str(int(sum(map(lambda x: int(x.text.strip()), [rating_items[1], rating_items[3], rating_items[5], rating_items[7]]))/4)) + '/5'
                    print(rating)
                except Exception as e:
                    rating = "0/5"
                    print(p, ligne)
                    print(e)

                try:
                    lang = detect(comment)
                except:
                    lang = 'en'

                self.reviews_data.append({
                    'comment': comment,
                    'language': lang,
                    'rating': "1/5",
                    'source': urlparse(self.url).netloc.split('.')[1],
                    # 'author': ', '.join([item.find_all('section')[0].find_all('p')[0].text.strip(), item.find_all('section')[0].find_all('p')[1].text.strip()]),
                    'establishment': '/api/establishments/2'
                })

                ligne += 1

            try:
                next_btn_div = self.driver.find_element(By.XPATH, "//div[@data-test='pagination-next']")
                
                if next_btn_div:
                    next_btn = next_btn_div.find_element(By.XPATH, "./..")

                    if next_btn.find_element(By.XPATH, "./..").is_displayed():
                        self.driver.execute_script("arguments[0].click();", next_btn)
                        time.sleep(5)
                    else:
                        print("Dernière page !!!")
                        break
                else:
                    print("Bouton non trouvé !!!")
                    break
                
            except Exception as e:
                print(e)
                break
        
            p += 1

        print(len(self.reviews_data))

        # self.data = reviews


trp = OpenTable()
trp.set_url("https://www.opentable.com/the-belvedere")
trp.execute()
# print(trp.data)