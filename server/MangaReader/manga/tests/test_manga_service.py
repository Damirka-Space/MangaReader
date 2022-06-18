import pytest

from ..services.chapter import Chapter
from ..services.source import MockedMangaSource

# NOTE fixture?
chapter = Chapter(
    source=MockedMangaSource,
    manga_name='one-piece',
    volume_serial=8,
    serial=71
)


@pytest.mark.django_db
def test_frames_cnt():
    assert chapter.frames_cnt == len(list(chapter.frames))


@pytest.mark.django_db
def test_incomplete_chapter():
    # [ ] if not all frames in chapter raise IncompleteChapterError
    pass


@pytest.mark.django_db
def test_chapter_existence():
    # [ ] if chapter isn't exist raise Exception
    pass


@pytest.mark.django_db
def test_get_chapter_if_exist():
    # [ ] if chapter already in db get it not create
    # NOTE if objects id equals
    pass
