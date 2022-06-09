from .. import models


class Manga:
    @classmethod
    def get_by_name_in_source(cls, name: str, source_id: int) -> models.Manga:
        try:
            return models.Manga.objects.get(name=name)
        except models.Manga.DoesNotExist:
            return cls.__create(name=name, source_id=source_id)

    @classmethod
    def __create(cls, name: str, source_id: int) -> models.Manga:
        manga, is_created = models.Manga.objects.get_or_create(
            name=name,
            volume_cnt=0,
            chapters_cnt=0,
            url='test.com/manga'
        )
        if is_created:
            manga.source_name.add(models.MangaSource.objects.get(id=source_id))
        return manga
