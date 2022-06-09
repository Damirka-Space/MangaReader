from .. import models


class Volume:
    @classmethod
    def get_or_create(cls, manga_id: int, serial: int) -> models.Volume:
        volume, is_created = models.Volume.objects.get_or_create(
            manga_id=models.Manga.objects.get(id=manga_id),
            serial=serial,
            chapter_start_serial=cls.get_start_chapter(),
            chapter_end_serial=cls.get_end_chapter()
        )
        return volume

    @classmethod
    def get_start_chapter(cls) -> int:
        return 0

    @classmethod
    def get_end_chapter(cls) -> int:
        return 0
