from typing import Any
from django.forms import model_to_dict

from ..models import Manga
from .source import ReadYagami, MangaLib
from .chapter import Chapter


def get_manga_list() -> list:
    return Manga.objects.all().values()


def create_new_manga_object(name: str, chapters_cnt: int) -> dict[str, Any]:
    return model_to_dict(Manga.objects.create(name=name,
                                              chapters_cnt=chapters_cnt))


def get_manga_chapter(name: str, volume_serial: int,
                      serial: int) -> dict:
    chapter = Chapter(MangaLib, name, volume_serial, serial)
    return {
        'name': chapter.manga_name,
        'source': {
            'url': chapter.source.url
        },
        'volume_serial': chapter.volume_serial,
        'serial': chapter.serial,
        'frames_cnt': chapter.frames_cnt,
        'frames_urls': ['http://localhost:8000/cdn/img/' + str(f.id)
                        for f in chapter.frames]  # FIXME get internal url
    }
