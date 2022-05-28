from abc import ABC, abstractmethod
from urllib.request import Request, urlopen
import logging

from bs4 import BeautifulSoup

from .. import models

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MangaSource(ABC):
    name: str
    url: str
    model = models.MangaSource
    tmp: dict[str, BeautifulSoup] = {}

    @classmethod
    def _get_webpage(cls, url: str,
                     headers: dict = {'User-Agent': 'Mozilla/5.0'}) -> bytes:
        logger.info('Visiting url: ' + url)
        return urlopen(Request(url, headers=headers)).read()

    @classmethod
    def _get_soup(cls, url: str, update: bool = False) -> BeautifulSoup:
        if url not in cls.tmp or update:
            cls.tmp[url] = BeautifulSoup(
                cls._get_webpage(url), 'html.parser')
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


class ReadYagami(MangaSource):
    name = 'ReadYagami'
    url = 'https://read.yagami.me/'

    @classmethod
    def _get_chapter_first_frame_url(cls, chapter_url: str) -> str:
        return cls._get_soup(chapter_url).select_one('#miku')['src']

    @classmethod
    def get_chapter_url(cls, manga_name: str, volume_serial: str,
                        chapter_serial: str) -> str:
        return cls.url + \
            f'read/{manga_name}/{volume_serial}/{chapter_serial}/'

    @classmethod
    def get_chapter_frames_cnt(cls, chapter_url: str) -> int:
        soup = cls._get_soup(chapter_url)
        div_block = list(soup.select_one('.dropdown_right').children)[0]
        return int(div_block.text[:-2])

    @classmethod
    def get_frame_url(cls, chapter_url: str, frame_num: int) -> str:
        first_frame_url = cls._get_chapter_first_frame_url(chapter_url)
        frame_serial = '0' * (3 - len(str(frame_num))) + str(frame_num)
        return '/'.join(first_frame_url.split('/')
                        [:-1]) + f'/{frame_serial}.jpg'
