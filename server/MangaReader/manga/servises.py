from django.forms import model_to_dict
from .models import Manga

from .manga_services import MangaSource


def get_manga_list() -> list:
    return Manga.objects.all().values()


def create_new_manga_object(name: str, chapters_cnt: int) -> None:
    return model_to_dict(Manga.objects.create(name=name,
                                              chapters_cnt=chapters_cnt))


def get_manga_chapter(name: str, volume_serial: str,
                      chapter_serial: int) -> dict:
    return {
        'name': name,
        'volume_serial': volume_serial,
        'chapter_serial': chapter_serial,
        'frames_cnt': MangaSource.get_chapter_frames_cnt(
            name, volume_serial, chapter_serial
        ),
        'frames_urls': MangaSource.get_chapter_frame_urls(
            name, volume_serial, chapter_serial
        )
    }
