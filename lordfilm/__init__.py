import logging
import os
import typing

import bs4
from seleniumrequests import Chrome
from bs4 import BeautifulSoup
import functools


class Movie:
    def __init__(self, url, _player_link=None, title=None, year=None, imdb_rate=None, kp_rate=None, img_link=None,
                 session=None):
        self.url = url
        self.img_link = img_link
        self.kp_rate = kp_rate
        self.imdb_rate = imdb_rate
        self.year = year
        self.title = title
        self._player_link = _player_link

        self.session = session

    @functools.lru_cache()
    def fetch_full_info(self) -> None:
        r = self.session.request("GET", self.url)
        soup = BeautifulSoup(r.content, 'html.parser')
        self._player_link = soup.select('.tabs-b.video-box')[1].find('iframe')['src']

    @property
    def player_link(self):
        return self._player_link


class LordFilm:
    def __init__(self, driver=None):
        self.session = driver
        if not driver:
            self.session = Chrome(
                executable_path=
                rf"{os.getcwd()}\chromedriver.exe")
        self.base_url = None

    def init(self):
        """update"""
        self.base_url = self.get_base_url()
        self.session.get(self.base_url)
        logging.info(f'cooks: {self.session.get_cookies()}')
        return self

    def get_base_url(self):
        url = 'https://www.google.com/url?q=https://lordfilm.vet/'
        self.session.get(url)
        el = self.session.find_element_by_xpath('//a')  # [href="https://lordfilm.vet/"]
        el.click()
        return self.session.current_url

    def search(self, query) -> typing.List[Movie]:
        url = self.base_url + '/index.php?do=search'
        payload = {'do': 'search',
                   'subaction': 'search',
                   'search_start': 0,
                   'full_search': 0,
                   'result_from': 1,
                   'story': query}
        r = self.session.request("POST", url, data=payload)
        return self.__parse_search_box(r.content)

    def __parse_search_box(self, content) -> typing.List[Movie]:
        soup = BeautifulSoup(content, 'html.parser')
        els = soup.find_all('div', {'class': 'th-item'})
        return [self.__parse_short_card(el) for el in els]

    def __parse_short_card(self, el: bs4.element.Tag) -> Movie:
        return Movie(title=el.find('div', {'class': 'th-title'}).text,
                     img_link=el.find('img')['src'],
                     url=el.find('a')['href'],
                     kp_rate=el.select_one('.th-rate-kp').text,
                     imdb_rate=el.select_one('.th-rate-imdb').text,
                     year=el.find('div', {'class': 'th-series'}).text,
                     session=self.session)

    def __del__(self):
        if self.session:
            self.session.quit()
