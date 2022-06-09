import logging
from typing import Generator

from .. import models
from .frame import FrameBrowser
from .manga import Manga
from .source.base import MangaSourceBase
from .volume import Volume

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

    @property
    def frames(self) -> Generator[models.Frame, None, None]:
        if self.__frame_browser.is_all_related_exist():
            for frame in self.__frame_browser.get_all_related():
                yield frame
        else:
            for serial in range(1, self.frames_cnt + 1):
                yield self._get_frame_by_serial(serial)

    @property
    def frames_cnt(self) -> int:
        logger.debug('getting frames cnt')
        return self._object.frames_cnt

    @property
    def _id(self):
        return self._object.id

    @property
    def _url(self) -> str:
        return self.source.get_chapter_url(
            self.manga_name, self.volume_serial, self.serial)

    @property
    def _object(self) -> models.Chapter:
        try:
            logger.debug('trying to get object')
            return self.__get_object()
        except models.Chapter.DoesNotExist:
            logger.debug('creating object')
            return self.__create_object()

    def _get_frame_by_serial(self, serial: int) -> models.Frame:
        logger.debug(f'get frame serial {serial}')
        if self.__frame_browser.is_exist(serial):
            return self.__frame_browser.get_by_serial(serial)
        return self.__frame_browser.create(
            serial, self.source.get_frame_url(self._url, serial))

    @property
    def __frame_browser(self) -> FrameBrowser:
        return FrameBrowser(self._id)

    @property
    def __manga_id(self) -> str:
        return Manga.get_by_name_in_source(self.manga_name, self.source.id).id

    def __get_object(self) -> models.Chapter:
        return models.Chapter.objects.get(
            volume_id=Volume.get_or_create(
                self.__manga_id, self.volume_serial),
            serial=self.serial,
        )

    def __create_object(self) -> models.Chapter:
        return models.Chapter.objects.create(
            source_name=models.MangaSource.objects.get(id=self.source.id),
            manga_id=models.Manga.objects.get(id=self.__manga_id),
            volume_id=Volume.get_or_create(
                self.__manga_id, self.volume_serial),
            serial=self.serial,
            frames_cnt=self.source.get_chapter_frames_cnt(self._url),
        )


class MockedChapter(Chapter):
    def _get_frame_by_serial(self, serial: int) -> models.Frame:
        return models.Frame.objects.create(
            chapter=self._object,
            serial=serial,
            external_url=self.source.get_frame_url(self._url, serial),
            internal_url='',
            img=b''
        )
