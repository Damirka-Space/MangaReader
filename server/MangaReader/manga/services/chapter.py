import logging
from typing import Generator

from .. import models
from .source.base import MangaSourceBase
from .frame import Frame

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
        self.object = self.__get_object()
        logger.debug('chapter object: ' + str(self.object))

    def __str__(self) -> str:
        return f'\nChapter::{self.source.url}::{self.manga_name}:: \
            {self.volume_serial}::{self.serial}'

    def __get_object(self):
        try:
            return models.Chapter.objects.get(
                volume_id=models.Volume.objects.get(id=1),
                serial=self.serial,
            )
        except:
            return models.Chapter.objects.create(
                source_name=models.MangaSource.objects.get(id=1),
                manga_id=models.Manga.objects.get(id=1),
                volume_id=models.Volume.objects.get(id=1),
                serial=self.serial,
                frames_cnt=self.get_frames_cnt(),
            )

    def _get_url(self) -> str:
        return self.source.get_chapter_url(
            self.manga_name, self.volume_serial, self.serial)

    def _get_frame_url(self, frame_num: int) -> str:
        return self.source.get_frame_url(self.url, frame_num)

    def get_frames_cnt(self):
        """get number of images related to chapter"""
        logger.debug('getting frames cnt')
        return self.source.get_chapter_frames_cnt(self.url)

    def get_frame_urls(self) -> list[str]:
        """get urls of images related to chapter from source"""
        logger.debug('getting frame urls for chapter' + str(self))
        frames_cnt = self.get_frames_cnt()
        return [self._get_frame_url(f) for f in range(1, frames_cnt + 1)]

    def get_frames(self) -> Generator[models.Frame, None, None]:
        if Frame.is_all_related_to_chapter_exist(self.object.id):
            for frame in Frame.get_all_related_to_chapter(self.object.id):
                yield frame
        else:
            for serial, url in enumerate(self.get_frame_urls()):
                logger.debug('get frame from ' + url)
                yield Frame(self.object.id, serial, url).object

    def get_frame_images(self) -> Generator[bytes, None, None]:
        """
        Get frames related to the chapter
        Return generator of images in bytes format
        Images could be jpg or png
        """
        for frame in self.get_frames():
            yield frame.img

    def get_frame_external_urls(self) -> Generator[str, None, None]:
        for frame in self.get_frames():
            yield frame.external_url
