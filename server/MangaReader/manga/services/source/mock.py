import random

from .base import MangaSourceBase


class MockedMangaSource(MangaSourceBase):
    name = 'MockedSource'
    url = 'https://source.mock/'

    @classmethod
    def get_chapter_url(cls, manga_name: str, volume_serial: str,
                        chapter_serial: str) -> str:
        return f'{cls.url}/{manga_name}/{volume_serial}/{chapter_serial}'

    @classmethod
    def get_chapter_frames_cnt(cls, chapter_url: str) -> int:
        return random.randint(16, 50)

    @classmethod
    def get_frame_url(cls, chapter_url: str, frame_serial: int) -> str:
        return chapter_url + '/' + str(frame_serial)

    @classmethod
    def get_frame_image(cls, chapter_url: str, frame_serial: int) -> bytes:
        frame_url = cls.get_frame_url(chapter_url, frame_serial)
        return bytes(frame_url, 'utf-8')
