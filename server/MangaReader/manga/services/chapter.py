import logging

from .source.base import MangaSourceBase

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Chapter:
    def __init__(self, source: MangaSourceBase, manga_name: str,
                 volume_serial: int, serial: int) -> None:
        self.source = source
        self.manga_name = manga_name
        self.volume_serial = volume_serial
        self.serial = serial
        self.url = self._get_url()

    def __str__(self) -> str:
        return f'\nChapter::{self.source.url}::{self.manga_name}:: \
            {self.volume_serial}::{self.serial}'

    def _get_url(self) -> str:
        return self.source.get_chapter_url(
            self.manga_name, self.volume_serial, self.serial)

    def _get_frame_url(self, frame_num: int) -> str:
        return self.source.get_frame_url(self.url, frame_num)

    def get_frames_cnt(self):
        logger.debug('getting frames cnt')
        return self.source.get_chapter_frames_cnt(self.url)

    def get_frame_urls(self) -> list[str]:
        logger.debug('getting frame urls for chapter' + str(self))
        frames_cnt = self.get_frames_cnt()
        return [self._get_frame_url(f) for f in range(1, frames_cnt + 1)]
