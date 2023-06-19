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


class TripAdvisor(Scraping):
    def __init__(self, in_background: bool = False, url: str = None):
        super().__init__(in_background=in_background, url=url)

    def extract(self):
        try:
            page = self.driver.page_source

            soupe = BeautifulSoup(page, 'lxml')

            info_container = soupe.find('div', {"data-tab":"TABS_OVERVIEW"}).find_all('div', class_='ui_column')
            website = info_container[2].find('div', class_='e').find('div', class_='f').find_all('a', href=True)

            name = soupe.find('h1', {'data-test-target':'top-info-header'}).text.strip()
            open_state = re.sub(r'[^\w\s:-]', '', soupe.find('div', {'data-test-target':'restaurant-detail-info'}).find('div', class_='NehmB').text.strip())
            info_container = soupe.find('div', {"data-tab":"TABS_OVERVIEW"}).find_all('div', class_='ui_column')
            stars = info_container[0].find('span', class_='ZDEqb').text.strip().replace(',', '.')
            review_count = int(info_container[0].find('a', class_='IcelI').text.strip().replace('\u202f', '').split(' ')[0])
            adresse = info_container[2].find_all('span', class_='yEWoV')[0].text.strip()
            website = info_container[2].find('div', class_='e').find('div', class_='f').find_all('a', href=True)[1]['href']

            phone_number = [item.text.strip() for item in info_container[2].find('div', class_='e').find('div', class_='f').find_all('a', href=True) if item['href'].startswith('tel:')][0] or ''

            reviews_container = soupe.find('div', {'id':"REVIEWS"}).find_all('div', class_='review-container')
            url = self.driver.current_url
            reviews = []

            for item in reviews_container:
                review = {}
                text = item.find('p', class_='partial_entry').text.strip()
                review['reviewsText'] = text
                review['reviewsRating'] = str(int(item.find('span', class_='ui_bubble_rating')['class'][1].split('_')[1]) / 10)
                try:
                    review['reviewLangage'] = detect(review['reviewsText'])
                except:
                    print("Erreur langue: ", review['reviewsText'])
                    review['reviewLangage'] = 'en'
                review['source'] = urlparse(url).netloc.split('.')[1]
                review['reviewsAuthorName'] = item.find('div', class_='info_text').text.strip()
                review['reviewsTime'] = item.find('span', class_='ratingDate').text.strip()
                reviews.append(review)

            # images = []

            # self.driver.execute_script("ta.plc_resp_rr_photo_mosaic_0_handlers.openPhotoViewer();")
            # WebDriverWait(self.driver, 10)
            # time.sleep(4)

            # subpage = BeautifulSoup(self.driver.page_source, 'lxml')
            # images_container = subpage.find('div', class_='photoGridBox').find_all('img', src=True)

            # for i in range(len(images_container)):
            #     image = images_container[i]['src']
            #     images.append(image)
            
            # image_button = check_images()
            # if image_button:
            #     self.driver.execute_script("arguments[0].click();", image_button)
            #     WebDriverWait(self.driver, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME,"photoGridBox"))

            #     subpage = BeautifulSoup(self.driver.page_source, 'lxml')
            #     images_container = subpage.find('div', class_='photoGridBox').find_all('img')

            #     for i in range(5):
            #         image = images_container[i]['src']
            #         images.append(image)

            data = {}
            data['name'] = name
            data['rating'] = stars
            data['reservable'] = ''
            data['takeout'] = True
            data['types'] = 'restaurant'
            data['url'] = url
            data['addresseComponentLongName'] = adresse
            data['website'] = website
            data['internationalPhone'] = phone_number
            # data['openingHoursOpenNow'] = ''
            # data['openingHoursPeriods'] = ''
            data['userRatingsTotal'] = review_count
            # data['images'] = images
            data['reviews'] = reviews

            self.data = data

        except Exception as e:
            print("erreur:", e)