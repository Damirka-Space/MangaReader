from abc import ABC, abstractmethod
from urllib.request import Request, urlopen
import logging

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
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
    def __get_selenium_driver(cls, show_browser: bool = False,
                              options: Options = None) -> Chrome:
        if not show_browser:
            options = Options()
            options.add_argument('--headless')
        return Chrome(
            '/usr/lib/chromium-browser/chromedriver',
            options=options)

    @classmethod
    def __get_webpage_with_selenium(cls, url: str) -> str:
        driver = cls.__get_selenium_driver()
        driver.get(url)
        html = driver.page_source
        driver.close()
        return html

    @classmethod
    def _get_webpage(cls, url: str,
                     headers: dict = {'User-Agent': 'Mozilla/5.0'},
                     with_selenium: bool = False) -> bytes | str:
        logger.info('Visiting url: ' + url)

        if not with_selenium:
            return urlopen(Request(url, headers=headers)).read()
        return cls.__get_webpage_with_selenium(url)

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
