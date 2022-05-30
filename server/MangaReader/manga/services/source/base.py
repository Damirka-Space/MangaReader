from abc import ABC, abstractmethod
from urllib.request import Request, urlopen
import logging

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from ... import models

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MangaSourceBase(ABC):
    name: str
    url: str
    model = models.MangaSource
    tmp: dict[str, BeautifulSoup] = {}

    @classmethod
    def _get_webpage(cls, url: str,
                     headers: dict = {'User-Agent': 'Mozilla/5.0'},
                     with_selenium: bool = False) -> bytes | str:
        logger.info('Visiting url: ' + url)

        if not with_selenium:
            return urlopen(Request(url, headers=headers)).read()

        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(
            '/usr/lib/chromium-browser/chromedriver', options=options)

        driver.get(url)
        html = driver.page_source
        driver.close()
        return html

    @classmethod
    def _get_soup(cls, url: str, update: bool = False,
                  with_selenium: bool = False) -> BeautifulSoup:
        if url not in cls.tmp or update:
            cls.tmp[url] = BeautifulSoup(
                cls._get_webpage(
                    url, with_selenium=with_selenium), 'html.parser')
        return cls.tmp[url]

    @classmethod
    @abstractmethod
    def get_chapter_url(cls, manga_name: str, volume_serial: str,
                        chapter_serial: str) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_chapter_frames_cnt(cls, chapter_url: str) -> int:
        pass

    @classmethod
    @abstractmethod
    def get_frame_url(cls, chapter_url: str, frame_num: int) -> str:
        pass
