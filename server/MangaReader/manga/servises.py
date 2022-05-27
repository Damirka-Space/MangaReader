from django.forms import model_to_dict
from .models import Manga

from .manga_service import MangaSource, Chapter


def get_manga_list() -> list:
    return Manga.objects.all().values()


def create_new_manga_object(name: str, chapters_cnt: int) -> None:
    return model_to_dict(Manga.objects.create(name=name,
                                              chapters_cnt=chapters_cnt))


def get_manga_chapter(name: str, volume_serial: str,
                      chapter_serial: int) -> dict:
    chapter = Chapter(MangaSource, name, volume_serial, chapter_serial)
    return {
        'name': chapter.manga_name,
        'source': {
            'url': chapter.source.url
        },
        'volume_serial': chapter.volume_serial,
        'chapter_serial': chapter.serial,
        'frames_cnt': chapter.get_frames_cnt(),
        'frames_urls': chapter.get_frame_urls()
    }
