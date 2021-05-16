import time
import dateparser
import hashlib

from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from typing import List


@dataclass
class Slot:
    id: str
    url: str
    center_name: str
    center_address: str
    date: datetime

    def __str__(self):
        s = self.center_name + '\n'
        s += self.center_address + '\n'
        s += f'{self.date.day}/{self.date.month} {self.date.hour}:{self.date.minute}' + '\n'
        s += self.url + '\n'
        return s

    __repr__ = __str__


def fetch_index(url: str) -> BeautifulSoup:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    return soup


def parse_available_slots(soup: BeautifulSoup) -> List[Slot]:
    slots = []
    for center in soup.find_all(class_='dl-search-result'):
        available_slots = center.find(class_='dl-search-result-calendar').find_all(class_='availabilities-slot')

        # Center has open slots
        if available_slots:
            url = center.find(class_='dl-search-result-name')['href']
            center_name = center.find(class_='dl-search-result-title').text
            center_address = center.find(class_='dl-search-result-content').find(class_='dl-text').text

            for slot in available_slots:
                date = dateparser.parse(slot['title'])
                id_str = center_name + str(date)
                id_hash = hashlib.md5(id_str.encode())
                id_ = id_hash.hexdigest()
                slots.append(Slot(
                    id=id_,
                    url=url,
                    center_name=center_name.replace('\n', ''),
                    center_address=center_address.replace('\n', ''),
                    date=date
                ))

    return slots


def get_available_slots(url) -> List[Slot]:
    soup = fetch_index(url)
    slots = parse_available_slots(soup)
    return slots
