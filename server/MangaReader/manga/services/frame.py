from typing import Generator
import requests
import logging

from .. import models
from .exceptions import IncompleteChapterError

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Frame:
    def __init__(self, chapter_id: int, serial: int, url: str) -> None:
        self.__chapter_id = chapter_id
        self.serial = serial
        self.external_url = url

    @property
    def chapter(self) -> models.Chapter:
        logger.debug('chapter object' + str(self.__chapter_id))
        return models.Chapter.objects.get(id=self.__chapter_id)

    @property
    def object(self) -> models.Frame:
        return self.__get_object()

    def __get_object(self) -> models.Frame:
        try:
            logger.debug('trying get object')
            return models.Frame.objects.get(
                chapter=self.chapter,
                serial=self.serial,
            )
        except models.Frame.DoesNotExist:
            logger.debug('creating object')
            return models.Frame.objects.create(
                chapter=self.chapter,
                serial=self.serial,
                external_url=self.external_url,
                internal_url='',
                img=self.__get_img_from_external_url()
            )

    def __get_img_from_external_url(self) -> bytes:
        logger.debug('downloading frame from ' + self.external_url)
        return requests.get(self.external_url).content


class FrameBrowser:
    def __init__(self, chapter_id: int) -> None:
        self.__chapter_id = chapter_id

    def create(self, serial: int,
               external_url: str) -> models.Frame:
        return Frame(self.__chapter_id, serial, external_url).object

    def is_exist(self, serial: int) -> bool:
        return models.Frame.objects.filter(
            chapter=self.__chapter_object,
            serial=serial
        ).count() > 0

    def get_by_serial(self, serial: int) -> models.Frame:
        return models.Frame.objects.get(chapter=self.__chapter_object,
                                        serial=serial)

    def is_all_related_exist(self) -> bool:
        chapter = self.__chapter_object
        return len(chapter.frame_set.all()) == chapter.frames_cnt

    def get_all_related(self) -> Generator[models.Frame, None, None]:
        if not self.is_all_related_exist():
            raise IncompleteChapterError()

        for frame in self.__chapter_object.frame_set.all():
            yield frame

    @property
    def __chapter_object(self) -> models.Chapter:
        return models.Chapter.objects.get(id=self.__chapter_id)
