from typing import Generator
import logging

from django.db.models import QuerySet

from .. import models
from .exceptions import IncompleteChapterError

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Frame:
    def __init__(self, chapter_id: int, serial: int, img: bytes) -> None:
        self.__chapter_id = chapter_id
        self.serial = serial
        self.img = img

    @property
    def chapter(self) -> models.Chapter:
        logger.debug('chapter object' + str(self.__chapter_id))
        return models.Chapter.objects.get(id=self.__chapter_id)

    @property
    def object(self) -> models.Frame:
        return self.__get_object()

    def __get_object(self) -> models.Frame:
        try:  # NOTE check its only creating not getting
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
                external_url='',  # [ ] delete
                internal_url=self.__get_internal_url(),
                img=self.img
            )

    def __get_internal_url(self):
        # [ ] Get from CDN
        # NOTE get host where project started
        # NOTE host + cdn/img/<id>
        return ''


class FrameBrowser:
    def __init__(self, chapter_id: int) -> None:
        self.__chapter_id = chapter_id

    @classmethod  # FIXME What is this?
    def get_by_id(cls, frame_id: int) -> models.Frame:
        return models.Frame.objects.get(id=frame_id)

    def create(self, serial: int, img: bytes) -> models.Frame:
        return Frame(self.__chapter_id, serial, img).object

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
        return len(self.__chapter_frame_set) == chapter.frames_cnt

    def get_all_related(self) -> Generator[models.Frame, None, None]:
        if not self.is_all_related_exist():
            raise IncompleteChapterError()

        for frame in self.__chapter_frame_set:
            yield frame

    @property
    def __chapter_frame_set(self) -> QuerySet:
        return self.__chapter_object.frame_set.all()

    @property
    def __chapter_object(self) -> models.Chapter:
        return models.Chapter.objects.get(id=self.__chapter_id)
