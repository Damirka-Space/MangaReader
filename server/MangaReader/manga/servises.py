from django.forms import model_to_dict
from .models import Manga


def get_manga_list() -> list:
    return Manga.objects.all().values()


def create_new_manga_object(name: str, chapters_cnt: int) -> None:
    return model_to_dict(Manga.objects.create(name=name,
                                              chapters_cnt=chapters_cnt))
