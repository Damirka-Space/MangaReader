from urllib.request import Request, urlopen, urlretrieve
import logging

from bs4 import BeautifulSoup

from .models import Manga

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MangaSource:
    url = 'https://read.yagami.me/'

    @classmethod
    def check_if_title_exist(cls, title_name: str) -> dict:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = cls.url + title_name
        logger.info('Visiting url: ' + url)
        try:
            req = Request(url, headers=headers)
            logger.debug(req)
            return {'exist': True}
        except:
            logger.debug('Failed')
            return {'exist': False}

    @classmethod
    def get_webpage(cls, url: str,
                    headers: dict = {'User-Agent': 'Mozilla/5.0'}):
        logger.info('Visiting url: ' + url)
        return urlopen(Request(url, headers=headers)).read()

    @classmethod
    def get_soup(cls, url: str):
        return BeautifulSoup(cls.get_webpage(url), 'html.parser')

    @classmethod
    def get_frame_url(cls, chapter_url: str, frame_num: int) -> str:
        url = chapter_url + frame_num
        return cls.get_soup(url).select_one('#miku')['src']

    @classmethod
    def _get_chapter_frames_cnt_by_first_page_url(
            cls, chapter_first_page_url: str) -> int:
        soup = cls.get_soup(chapter_first_page_url)
        div_block = list(soup.select_one('.dropdown_right').children)[0]
        return int(div_block.text[:-2])

    @classmethod
    def get_chapter_first_page_url(cls, manga_name: str,
                                   volume_serial: str, chapter_serial: str) -> str:
        return cls.url +  \
            f'/read/{manga_name}/{volume_serial}/{chapter_serial}/page/1'

    @classmethod
    def get_chapter_frames_cnt(cls, manga_name: str,
                               volume_serial: str, chapter_serial: str) -> int:
        first_page_url = cls.get_chapter_first_page_url(
            manga_name, volume_serial, chapter_serial)
        return cls._get_chapter_frames_cnt_by_first_page_url(first_page_url)

    @classmethod
    def get_chapter_frame_urls(cls, manga_name: str,
                               volume_serial: int, chapter_serial: int) -> list[str]:
        first_frame_url = cls.get_chapter_first_page_url(
            manga_name, volume_serial, chapter_serial)
        frames_cnt = cls._get_chapter_frames_cnt_by_first_page_url(
            first_frame_url)
        chapter_url = cls.url + \
            f'/read/{manga_name}/{volume_serial}/{chapter_serial}/page/'
        frame_urls_list = []
        for frame_num in range(1, frames_cnt):
            frame_urls_list.append(
                cls.get_frame_url(chapter_url, str(frame_num)))
        return frame_urls_list
