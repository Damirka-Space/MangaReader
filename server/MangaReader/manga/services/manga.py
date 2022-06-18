from .. import models


class Manga:  # NOTE MangaBrowser?
    @classmethod
    def get_by_name_in_source(cls, name: str, source_id: int) -> models.Manga:
        try:
            return models.Manga.objects.get(name=name)
        except models.Manga.DoesNotExist:
            return cls.__create(name=name, source_id=source_id)

    @classmethod  # NOTE Should be not classmethod
    def __create(cls, name: str, source_id: int) -> models.Manga:
        manga, is_created = models.Manga.objects.get_or_create(
            name=name,
            volume_cnt=cls.__get_volume_cnt(),
            chapters_cnt=cls.__get_chapter_cnt(),
            url='test.com/manga'  # [ ] Valid url
        )
        if is_created:
            manga.source_name.add(models.MangaSource.objects.get(id=source_id))
        return manga

    @classmethod
    def __get_volume_cnt(cls) -> int:
        # [ ]  Get from source
        return 0

    @classmethod
    def __get_chapter_cnt(cls) -> int:
        # [ ] Get from source
        return 0
