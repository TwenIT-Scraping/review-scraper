from scraping import Scraping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from abc import abstractmethod
import sys
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from langdetect import detect



class Hotels(Scraping):

    def __init__(self, in_background: bool = False, url: str = "") -> None:
        super().__init__(in_background, url=url)
        self.url = url 
        self.reviews = []

    def close_popup(self) -> None:
        try:
            self.driver.find_element(By.CLASS_NAME, 'osano-cm-button--type_accept').click()
        except:
            pass

    def load_reviews(self) -> None:
        self.close_popup()
        button_review = self.driver.find_element(By.CSS_SELECTOR, '#Reviews > div > div > div:nth-child(2) > div > button')
        try:
            button_review.click()
            time.sleep(2)
            button_view_more = self.driver.find_element(By.CSS_SELECTOR, '#app-layer-reviews-property-reviews-1 > section > div.uitk-sheet-content.uitk-sheet-content-padded.uitk-sheet-content-extra-large > div > div.uitk-layout-grid.uitk-layout-grid-align-content-start.uitk-layout-grid-has-auto-columns.uitk-layout-grid-has-columns.uitk-layout-grid-has-space.uitk-layout-grid-display-grid.uitk-layout-grid-item.uitk-layout-grid-item-has-column-start.uitk-layout-grid-item-has-column-start-by-medium.uitk-layout-grid-item-has-column-start-by-large.uitk-layout-grid-item-has-column-start-by-extra_large > div.uitk-layout-grid-item > section > div.uitk-spacing.uitk-type-center.uitk-spacing-margin-block-three > button')
            while button_view_more.is_displayed():
                button_view_more.click()
                WebDriverWait(self.driver, 5)
                time.sleep(1)
        except: 
            pass

    def extract(self) -> None:

        self.load_reviews()

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        reviews = soup.find('div', {'data-stid':'property-reviews-list'}).find_all('article', {'itemprop':'review'})
        for review in reviews:
            data = {}
            data['date_post'] = review.find('span', {'itemprop':'datePublished'}).text.strip()
            data['author'] = review.find('img').parent.text.split(',')[0]
            data['rating'] = review.find('span', {'itemprop':'ratingValue'}).text.split(' ')[0]
            data['comment'] = review.find('span', {'itemprop':'description'}).text if review.find('span', {'itemprop':'description'}) else ''
            self.reviews.append(data)


trp = Hotels(url="https://fr.hotels.com/ho1100722624/okko-hotels-paris-gare-de-l-est-paris-france")
trp.execute()