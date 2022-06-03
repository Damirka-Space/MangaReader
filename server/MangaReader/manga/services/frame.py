from asyncio.log import logger
import requests
import logging

from .. import models

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Frame:
    def __init__(self, chapter_id: int, serial: int, url: str) -> None:
        self.chapter = models.Chapter.objects.get(id=chapter_id)
        logger.debug('chapter object' + str(self.chapter))
        self.serial = serial
        self.external_url = url
        self.internal_url = ''
        self.img = b''
        self.object = self.__get_object()

    def __get_object(self) -> None:
        try:
            logger.debug('trying get object')
            return models.Frame.objects.get(
                chapter=self.chapter,
                serial=self.serial,
                external_url=self.external_url
            )
        except:
            logger.debug('creating object')
            return models.Frame.objects.create(
                chapter=self.chapter,
                serial=self.serial,
                external_url=self.external_url,
                internal_url=self.internal_url,
                img=self.__get_img_from_external_url()
            )

    def __get_img_from_external_url(self) -> bytes:
        return requests.get(self.external_url).content

    def get_img(self) -> bytes:
        return self.object.img
