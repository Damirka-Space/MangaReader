from bs4 import BeautifulSoup

from .base import MangaSourceBase


class MangaLib(MangaSourceBase):
    name = 'MangaLib'
    url = 'https://mangalib.me/'

    @classmethod
    def _get_soup(cls, url: str, update: bool = False,
                  with_selenium: bool = True) -> BeautifulSoup:
        return super()._get_soup(url, update, with_selenium)

    @classmethod
    def _get_page_url(cls, chapter_url: str, page_num: int) -> str:
        return f'{chapter_url}?page={page_num}'

    @classmethod
    def get_chapter_url(cls, manga_name: str, volume_serial: str,
                        chapter_serial: str) -> str:
        return cls.url + f'{manga_name}/v{volume_serial}/c{chapter_serial}'

    @classmethod
    def get_chapter_frames_cnt(cls, chapter_url: str) -> int:
        return len(cls._get_soup(chapter_url).select('option'))

    @classmethod
    def get_frame_url(cls, chapter_url: str, frame_num: int) -> str:
        soup = cls._get_soup(cls._get_page_url(chapter_url, frame_num))
        return soup.find_all('img')[frame_num - 1]['src']
