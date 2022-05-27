from urllib.request import Request, urlopen
import logging

from bs4 import BeautifulSoup

from . import models

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MangaSource:
    url = 'https://read.yagami.me/'
    model = models.MangaSource.objects.update_or_create(
        name='ReadYagami', url=url)
    tmp = {}

    @classmethod
    def _get_webpage(cls, url: str,
                     headers: dict = {'User-Agent': 'Mozilla/5.0'}) -> bytes:
        logger.info('Visiting url: ' + url)
        return urlopen(Request(url, headers=headers)).read()

    @classmethod
    def _get_soup(cls, url: str) -> BeautifulSoup:
        return BeautifulSoup(cls._get_webpage(url), 'html.parser')

    @classmethod
    def _get_chapter_frames_cnt_by_first_page_url(
            cls, chapter_first_page_url: str) -> int:
        soup = cls._get_soup(chapter_first_page_url)
        div_block = list(soup.select_one('.dropdown_right').children)[0]
        return int(div_block.text[:-2])

    @classmethod
    def _get_chapter_first_page_url(cls, chapter_url: str) -> str:
        return f'{chapter_url}page/1'

    @classmethod
    def _get_chapter_first_frame_url(cls, chapter_url: str) -> str:
        if chapter_url not in cls.tmp:
            url = chapter_url + 'page/1'
            first_frame_url = cls._get_soup(url).select_one('#miku')['src']
            cls.tmp[chapter_url] = first_frame_url
            return first_frame_url
        return cls.tmp[chapter_url]

    @classmethod
    def check_if_title_exist(cls, title_name: str,
                             headers={'User-Agent': 'Mozilla/5.0'}) -> bool:
        url = cls.url + title_name
        logger.info('Visiting url: ' + url)
        try:
            req = Request(url, headers=headers)
            logger.debug(req)
            return True
        except:
            logger.debug('Failed')
            return False

    @classmethod
    def add_title_if_not_exist(cls, manga_name: str) -> None:
        logging.debug('Creating manga object')
        # models.Manga.objects.update_or_create()

    @classmethod
    def get_frame_url(cls, chapter_url: str, frame_num: int) -> str:
        first_frame_url = cls._get_chapter_first_frame_url(chapter_url)
        frame_serial = '0' * (3 - len(str(frame_num))) + str(frame_num)
        return '/'.join(first_frame_url.split('/')
                        [:-1]) + f'/{frame_serial}.jpg'

    @classmethod
    def get_chapter_frames_cnt(cls, chapter_url: str) -> int:
        return cls._get_chapter_frames_cnt_by_first_page_url(
            cls._get_chapter_first_page_url(chapter_url))

    @classmethod
    def get_chapter_url(cls, manga_name: str, volume_serial: str,
                        chapter_serial: str) -> str:
        return cls.url + \
            f'read/{manga_name}/{volume_serial}/{chapter_serial}/'


class Chapter:
    def __init__(self, source: MangaSource, manga_name: str,
                 volume_serial: int, serial: int) -> None:
        self.source = source
        self.manga_name = manga_name
        self.volume_serial = volume_serial
        self.serial = serial
        self.url = self._get_url()

    def _get_url(self) -> str:
        return self.source.get_chapter_url(
            self.manga_name, self.volume_serial, self.serial)

    def _get_frame_url(self, frame_num: int) -> str:
        return self.source.get_frame_url(self.url, str(frame_num))

    def get_frames_cnt(self):
        return self.source.get_chapter_frames_cnt(self.url)

    def get_frame_urls(self) -> list[str]:
        frames_cnt = self.get_frames_cnt()
        return [self._get_frame_url(f) for f in range(1, frames_cnt)]
